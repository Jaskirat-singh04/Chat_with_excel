import google.generativeai as genai
from database import sql_query
import os

schema_description = '''
[
    {"table": "mytable", "columns": [
        {"name": "Site", "type": "string"},
        {"name": "Date", "type": "datetime"},
        {"name": "Invoice Number", "type": "string"},
        {"name": "Customer Code", "type": "string"},
        {"name": "Name", "type": "string"},
        {"name": "Item Code", "type": "string"},
        {"name": "Item Description", "type": "string"},
        {"name": "Quantity", "type": "int"}
    ]}
]
'''

def setup_chat_agent(conn):
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)

    def sql_tool(query: str):
        return sql_query(query, conn)

    system_prompt = f"""
    You are an expert SQL analyst. Generate SQL queries based on the user question and the database schema.
    Use the 'sql_query' tool to run the query and return accurate results.

    {schema_description}
    """.strip()

    model = genai.GenerativeModel("gemini-1.5-flash", tools=[sql_tool], system_instruction=system_prompt)
    return model.start_chat(enable_automatic_function_calling=True)

def ask_question(chat, question):
    return chat.send_message(question).text
