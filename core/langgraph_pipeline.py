from langgraph.graph import StateGraph, END

from core.graph_state import GraphState
from core.agent_nodes import (
    schema_node,
    sql_generation_node,
    execution_node,
    narrator_node,
    chart_node,
    correction_node
)


class LangGraphPipeline:
    
    def __init__(self):

        workflow = StateGraph(GraphState)

        workflow.add_node("schema", schema_node)
        workflow.add_node("sql", sql_generation_node)
        workflow.add_node("execute", execution_node)
        workflow.add_node("correct", correction_node)
        workflow.add_node("narrate", narrator_node)
        workflow.add_node("chart", chart_node)

        workflow.set_entry_point("schema")

        workflow.add_edge("schema", "sql")
        workflow.add_edge("sql", "execute")

        workflow.add_conditional_edges(
            "execute",
            lambda state: "error" if state["error"] else "success",
            {
                "error": "correct",
                "success": "narrate"
            }
        )

        workflow.add_edge("correct", "execute")
        workflow.add_edge("narrate", "chart")
        workflow.add_edge("chart", END)

        self.graph = workflow.compile()

    def run(self, question, state=None):
    
        if state is None:

            state = {
                "question": question,
                "conversation_history": [],
                "previous_sql": None
            }

        else:

            state["question"] = question

        state["conversation_history"].append(question)

        result = self.graph.invoke(state)

        result["previous_sql"] = result.get("sql")

        return result