from sqlalchemy import create_engine


class DBConnectionManager:

    def __init__(self):
        self.engine = None


    def connect_sqlite(self, filepath):

        connection_string = f"sqlite:///{filepath}"
        self.engine = create_engine(connection_string)

        return self.engine


    def connect_mysql(self, host, user, password, database):

        connection_string = (
            f"mysql+pymysql://{user}:{password}@{host}/{database}"
        )

        self.engine = create_engine(connection_string)

        return self.engine


    def connect_postgres(self, host, user, password, database):

        connection_string = (
            f"postgresql+psycopg2://{user}:{password}@{host}/{database}"
        )

        self.engine = create_engine(connection_string)

        return self.engine