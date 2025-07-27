import google.generativeai as genai
from database import sql_query
import os

# Configure API once at module level
API_CONFIGURED = False

def setup_chat_agent(conn, schema_description):
    global API_CONFIGURED
    
    # Configure API only once
    if not API_CONFIGURED:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        genai.configure(api_key=api_key)
        API_CONFIGURED = True

    def sql_tool(query: str):
        return sql_query(query, conn)

    system_prompt = f"""
    You are an expert data analyst. Your job is to answer questions about data by:
    1. Understanding the user's question
    2. Writing appropriate SQL queries using the sql_tool
    3. Interpreting the results and presenting them in clear, natural language
    
    Database Schema:
    {schema_description}
    
    Important guidelines:
    - The table name is 'mytable'
    - Use proper SQL syntax for SQLite
    - When referencing column names with spaces, use double quotes around them (e.g., "Invoice Number")
    - ALWAYS use the sql_tool to execute queries
    - NEVER show the SQL query to the user - only show the interpreted results
    - Present results in a clear, conversational manner
    - If results are numerical, provide context and summary
    - If there are multiple rows, summarize appropriately
    """.strip()

    model = genai.GenerativeModel("gemini-1.5-flash", tools=[sql_tool], system_instruction=system_prompt)
    return model.start_chat(enable_automatic_function_calling=True)

def ask_question(chat, question):
    return chat.send_message(question).text
