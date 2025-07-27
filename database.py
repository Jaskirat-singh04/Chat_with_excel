import sqlite3
import pandas as pd

def create_connection(db_name=":memory:"):
    return sqlite3.connect(db_name)

def load_excel_to_sql(df, conn, table_name="mytable"):
    df.to_sql(table_name, conn, if_exists="replace", index=False)

def sql_query(query: str, conn):
    """Run a SQL SELECT query on the database and return the results."""
    try:
        result = pd.read_sql_query(query, conn)
        return result.to_dict(orient='records')
    except Exception as e:
        return [{"error": str(e)}]
