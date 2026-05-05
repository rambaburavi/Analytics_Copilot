from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import re
import pandas as pd


class NarratorAgent:

    def __init__(self, model=None, tokenizer=None):
        pass


    def dataframe_to_text(self, df, question, style="executive_summary"):

        if df.empty:
            return "No results found for this query."

        columns = list(df.columns)

        num_cols = df.select_dtypes(include="number").columns.tolist()
        cat_cols = df.select_dtypes(include="object").columns.tolist()


        # Case 1 — ranking outputs
        if len(columns) == 1:

            top_value = df.iloc[0, 0]

            return (
                f"The dataset ranks results by **{columns[0]}**. "
                f"The top entry is **{top_value}**, indicating the strongest contribution."
            )


        # Case 2 — category vs metric
        if len(cat_cols) == 1 and len(num_cols) == 1:

            top_row = df.iloc[0]

            return (
                f"**{top_row[cat_cols[0]]}** shows the highest **{num_cols[0]}**, "
                "making it the leading contributor in this analysis."
            )


        # Case 3 — time series
        if "date" in columns[0].lower() or "month" in columns[0].lower():

            return (
                "This visualization shows how the metric changes over time, "
                "highlighting trends and seasonal variation across periods."
            )


        # Case 4 — correlation
        if len(num_cols) >= 2:

            return (
                f"There is a measurable relationship between **{num_cols[0]}** "
                f"and **{num_cols[1]}**, useful for identifying performance patterns."
            )


        return "The query successfully returned structured analytical results."