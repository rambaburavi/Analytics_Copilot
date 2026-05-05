from sqlalchemy import create_engine
import pandas as pd


class SQLExecutor:

    def __init__(self, db_path="database.db"):

        self.engine = create_engine(f"sqlite:///{db_path}")


    def execute(self, query):

        return pd.read_sql(query, self.engine)