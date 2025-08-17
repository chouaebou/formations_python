import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# ensemble des fonctions utilisables
class ConnectionHandler:

    def __init__(self, host, port, user, password, dbname, driver):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.dbname = dbname
        self.driver = driver

    def connectionDB(self):
        #connection_string = f"DRIVER={driver};SERVER={self.host};PORT={self.port};DATABASE={self.dbname};UID={self.user};PWD={self.password}"
        connection_string = f'DRIVER={self.driver};SERVER={self.host};PORT={self.port};DATABASE={self.dbname};Trusted_Connection=yes'
        connection_url = URL.create('mssql+pyodbc', query={'odbc_connect': connection_string})
        engine = create_engine(connection_url, use_setinputsizes=False, echo=False)
        #db_connection = engine.connect()
        return engine

    def fetch_data(self, query, connection):
        return pd.read_sql(query, con=connection)
    
    def insert_data(self, df, tablename, connection):
        df.to_sql(tablename, if_exists='append', index=False, con=connection)

    def execute_query(self, query, connection):
        connection.execute(query)

    def __del__(self):
        try:
            self.connectionDB().close()
        except:
            None