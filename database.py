import sqlite3
import pandas as pd

def create_connection(db_name=":memory:"):
    # Enable thread safety and WAL mode for better concurrent access
    conn = sqlite3.connect(
        db_name, 
        check_same_thread=False,  # Allow connection to be used across threads
        timeout=30.0             # Add timeout for database locks
    )
    # Enable WAL mode for better concurrency (if not in-memory)
    if db_name != ":memory:":
        conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")  # Balance between safety and speed
    return conn

def load_excel_to_sql(df, conn, table_name="mytable"):
    df.to_sql(table_name, conn, if_exists="replace", index=False)

def sql_query(query: str, conn):
    """Run a SQL SELECT query on the database and return the results."""
    try:
        # Ensure connection is still valid
        conn.execute("SELECT 1")  # Test connection
        result = pd.read_sql_query(query, conn)
        return result.to_dict(orient='records')
    except sqlite3.Error as e:
        return [{"error": f"Database error: {str(e)}"}]
    except Exception as e:
        return [{"error": f"Query error: {str(e)}"}]

def get_schema_from_dataframe(df, table_name="mytable"):
    """Generate schema description from DataFrame for LLM agent."""
    columns = []
    for col in df.columns:
        # Determine data type based on pandas dtype
        dtype = str(df[col].dtype)
        if 'int' in dtype:
            col_type = "int"
        elif 'float' in dtype:
            col_type = "float"
        elif 'datetime' in dtype:
            col_type = "datetime"
        elif 'bool' in dtype:
            col_type = "boolean"
        else:
            col_type = "string"
        
        columns.append({"name": col, "type": col_type})
    
    schema = [{"table": table_name, "columns": columns}]
    return str(schema)
