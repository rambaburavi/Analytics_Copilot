from typing import TypedDict, Optional, List
import pandas as pd


class GraphState(TypedDict):

    question: str

    schema: Optional[str]
    sql: Optional[str]
    corrected_sql: Optional[str]
    error: Optional[str]

    dataframe: Optional[pd.DataFrame]
    explanation: Optional[str]
    chart_type: Optional[str]

    conversation_history: Optional[List[str]]
    previous_sql: Optional[str]