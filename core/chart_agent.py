import pandas as pd
import plotly.express as px


class ChartAgent:

    def recommend_chart(self, df: pd.DataFrame, title="Analysis Result"):

        if df.empty:
            return None, "empty"


        num_cols = df.select_dtypes(include="number").columns.tolist()
        cat_cols = df.select_dtypes(include="object").columns.tolist()


        # CASE 1 — time series detection
        if len(num_cols) == 1 and len(df.columns) >= 2:

            if "date" in df.columns[0].lower() or "month" in df.columns[0].lower():

                chart = px.line(
                    df,
                    x=df.columns[0],
                    y=num_cols[0],
                    title=title,
                    markers=True
                )

                chart.update_layout(
                    template="plotly_dark",
                    height=420,
                    margin=dict(l=40, r=20, t=60, b=40),
                    font=dict(size=14)
                )

                return chart, "line"


        # CASE 2 — category vs metric
        if len(cat_cols) == 1 and len(num_cols) == 1:

            chart = px.bar(
                df,
                x=cat_cols[0],
                y=num_cols[0],
                title=title
            )

            chart.update_layout(
                template="plotly_dark",
                height=420
            )

            return chart, "bar"


        # CASE 3 — ranking only column
        if len(df.columns) == 1:

            chart = px.bar(
                df.reset_index(),
                x="index",
                y=df.columns[0],
                title=title
            )

            chart.update_layout(template="plotly_dark")

            return chart, "bar"


        # CASE 4 — numeric correlation
        if len(num_cols) >= 2:

            chart = px.scatter(
                df,
                x=num_cols[0],
                y=num_cols[1],
                title=title
            )

            chart.update_layout(template="plotly_dark")

            return chart, "scatter"


        return None, "none"