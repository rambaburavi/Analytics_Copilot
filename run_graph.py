from core.langgraph_pipeline import LangGraphPipeline


pipeline = LangGraphPipeline()

state = None

while True:

    question = input("\nAsk your analytics question: ")

    if question.lower() == "exit":
        break

    state = pipeline.run(question, state)

    print("\nExplanation:\n", state.get("explanation"))
    print("\nChart type:\n", state.get("chart_type"))