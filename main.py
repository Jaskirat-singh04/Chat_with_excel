# main.py
import streamlit as st
import pandas as pd
from database import create_connection, load_excel_to_sql
from llm_agent import setup_chat_agent, ask_question
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure page metadata
st.set_page_config(
    page_title="AI-Powered Document QA Agent",
    page_icon="📄",
    layout="centered"
)

# Title and description
st.title("AI Agent for QA on Shared Excel Documents")
st.markdown("""
This application lets you upload Excel-based documents and ask natural language questions about the data.
It uses Google's Gemini LLM to convert your questions into SQL queries and return meaningful answers.
""")

# File uploader section
uploaded_file = st.file_uploader("Upload an Excel document", type=["xlsx", "xls"])

if uploaded_file:
    try:
        # Load Excel file into DataFrame
        df = pd.read_excel(uploaded_file)

        if df.empty:
            st.warning("The uploaded document appears to be empty.")
        else:
            st.success("Document loaded successfully!")
            st.dataframe(df.head(), use_container_width=True)

            # Create SQLite DB and load table
            conn = create_connection("mydatabase.db")
            load_excel_to_sql(df, conn)

            # Set up LLM agent with SQL query tool
            chat = setup_chat_agent(conn)

            # Question input field
            user_question = st.text_input(
                "Ask a question about your data:",
                placeholder="e.g., What is the total quantity bought by H-MEDIX PHARMACY LTD?"
            )

            if user_question:
                with st.spinner("Generating answer..."):
                    try:
                        answer = ask_question(chat, user_question)
                        st.markdown("### Answer")
                        st.write(answer)
                    except Exception as e:
                        st.error(f"An error occurred while generating the response: {e}")

    except Exception as e:
        st.error(f"Failed to process the uploaded document: {e}")
else:
    st.info("Upload an Excel document to begin.")
