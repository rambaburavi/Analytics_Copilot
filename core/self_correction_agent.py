class SelfCorrectionAgent:
    
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def correct_sql(self, question, sql, error_message, schema):

        prompt = f"""
You are a SQL debugging assistant.

User question:
{question}

Schema:
{schema}

Generated SQL:
{sql}

Error message:
{error_message}

Fix the SQL query.
Return ONLY corrected SQL.
"""

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt"
        ).to(self.model.device)

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=120
        )

        corrected_sql = self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )

        return corrected_sql.strip()