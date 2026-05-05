from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import re

from core.chart_agent import ChartAgent
from core.narrator_agent import NarratorAgent
from core.schema_retriever import SchemaRetriever
from core.sql_executor import SQLExecutor
from core.self_correction_agent import SelfCorrectionAgent


BASE_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"
ADAPTER_PATH = "models/mistral_sql_agent_lora"


class SQLAgentPipeline:

    def __init__(self):

        print("Loading schema retriever...")
        self.schema_retriever = SchemaRetriever()

        print("Loading SQL executor...")
        self.executor = SQLExecutor()

        print("Loading tokenizer...")
        self.tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)

        print("Loading base model...")
        self.model = AutoModelForCausalLM.from_pretrained(
            BASE_MODEL,
            load_in_4bit=True,
            device_map="auto"
        )

        print("Loading SQL adapter...")
        self.model = PeftModel.from_pretrained(
            self.model,
            ADAPTER_PATH
        )

        print("Initializing narrator agent...")
        self.narrator = NarratorAgent(self.model, self.tokenizer)

        print("Initializing chart agent...")
        self.chart_agent = ChartAgent()

        print("Initializing self-correction agent...")
        self.corrector = SelfCorrectionAgent(self.model, self.tokenizer)


    # =========================
    # SQL Generation
    # =========================

    def generate_sql(self, question):

        schema_context = self.schema_retriever.retrieve(question)

        schema_text = "\n".join(schema_context[:6])

        prompt = f"""
### Instruction:
Generate a correct SQL query.

Rules:
- If GROUP BY is used → MUST include aggregation (SUM, COUNT, AVG)
- Do NOT select raw columns with GROUP BY
- Only use columns from schema
- Output ONLY SQL (no explanation)

Schema:
{schema_text}

Question:
{question}

### Response:
"""

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt"
        ).to(self.model.device)

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=80,
            do_sample=False,
            eos_token_id=self.tokenizer.eos_token_id
        )

        response = self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )

        match = re.search(
            r"(SELECT[\s\S]*?)(?:;|\n|###|$)",
            response,
            re.IGNORECASE
        )

        return match.group(1).strip() if match else response.strip()


    # =========================
    # Query Execution Pipeline
    # =========================

    def run(self, question):

        sql = self.generate_sql(question)

        print("\nGenerated SQL:\n", sql)


        # =========================
        # FIX: monthly aggregation correction
        # =========================

        if "GROUP BY strftime('%Y'" in sql and "SUM(" not in sql:

            sql = sql.replace(
                "SELECT revenue",
                "SELECT strftime('%Y-%m', order_date) AS month, SUM(revenue) AS revenue"
            )

            sql = sql.replace(
                "GROUP BY strftime('%Y', order_date) , strftime('%m', order_date)",
                "GROUP BY month ORDER BY month"
            )


        final_sql = sql


        try:

            df = self.executor.execute(sql)

        except Exception as e:

            print("\nSQL Error detected. Attempting correction...")

            schema_context = self.schema_retriever.retrieve(question)

            corrected_sql = self.corrector.correct_sql(
                question,
                sql,
                str(e),
                schema_context
            )

            match = re.search(
                r"(SELECT[\s\S]+?)(?:$|\n\n|###)",
                corrected_sql,
                re.IGNORECASE
            )

            if match:
                corrected_sql = match.group(1).strip()
            else:
                raise Exception("Failed to extract corrected SQL")


            # SQLite compatibility fixes
            corrected_sql = corrected_sql.replace(
                "YEAR(",
                "strftime('%Y', "
            )

            corrected_sql = corrected_sql.replace(
                "MONTH(",
                "strftime('%m', "
            )


            print("\nCorrected SQL:\n", corrected_sql)

            df = self.executor.execute(corrected_sql)

            final_sql = corrected_sql


        print("\nQuery Result:\n", df)


        explanation = self.narrator.dataframe_to_text(
            df,
            question,
            style="executive_summary"
        )

        print("\nNarrator Insight:\n", explanation)


        chart, chart_type = self.chart_agent.recommend_chart(
            df,
            title=question
        )

        chart_json = None

        if chart:
            chart_json = chart.to_json()


        return final_sql, df, explanation, chart_json


    # =========================
    # SQLite Connector
    # =========================

    def connect_sqlite(self, db_path):

        print(f"Connecting to SQLite DB: {db_path}")

        self.executor = SQLExecutor(db_path)

        print("SQLite connected successfully.")


# =========================
# Local Test Entry
# =========================

if __name__ == "__main__":

    agent = SQLAgentPipeline()

    question = "Monthly sales trend"

    agent.run(question)