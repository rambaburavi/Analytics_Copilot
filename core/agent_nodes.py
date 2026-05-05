from core.schema_retriever import SchemaRetriever
from core.sql_executor import SQLExecutor
from core.shared_pipeline import shared_pipeline


schema_agent = SchemaRetriever()
executor_agent = SQLExecutor()


def schema_node(state):

    question = state["question"]

    schema = schema_agent.retrieve(question)

    state["schema"] = "\n".join(schema)

    return state


def sql_generation_node(state):
    
    question = state["question"]

    previous_sql = state.get("previous_sql")

    if previous_sql:

        question = f"""
Previous SQL:
{previous_sql}

Follow-up question:
{question}
"""

    sql = shared_pipeline.generate_sql(question)

    state["sql"] = sql

    return state


def execution_node(state):

    sql = state["sql"]

    try:

        df = executor_agent.execute(sql)

        state["dataframe"] = df
        state["error"] = None

    except Exception as e:

        state["error"] = str(e)

    return state


def narrator_node(state):

    explanation = shared_pipeline.narrator.dataframe_to_text(
        state["dataframe"],
        state["question"]
    )

    state["explanation"] = explanation

    return state


def chart_node(state):

    chart, chart_type = shared_pipeline.chart_agent.recommend_chart(
        state["dataframe"]
    )

    state["chart_type"] = chart_type

    return state


def correction_node(state):

    corrected_sql = shared_pipeline.corrector.correct_sql(
        state["question"],
        state["sql"],
        state["error"],
        state["schema"]
    )

    state["sql"] = corrected_sql

    return state