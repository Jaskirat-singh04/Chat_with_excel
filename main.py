# main.py
import streamlit as st
import pandas as pd
from database import create_connection, load_excel_to_sql, get_schema_from_dataframe
from llm_agent import setup_chat_agent, ask_question
from dotenv import load_dotenv
import os
import hashlib
import time

# Load environment variables
load_dotenv()

# Configure page metadata
st.set_page_config(
    page_title="AI-Powered Document QA Agent",
    page_icon="📄",
    layout="centered"
)

# Initialize session state
if 'chat_agent' not in st.session_state:
    st.session_state.chat_agent = None
if 'conn' not in st.session_state:
    st.session_state.conn = None
if 'current_file_name' not in st.session_state:
    st.session_state.current_file_name = None
if 'db_file' not in st.session_state:
    st.session_state.db_file = None

def get_unique_db_name():
    """Generate a unique database name for this session"""
    timestamp = str(int(time.time() * 1000))
    return f"temp_db_{timestamp}.db"

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
        # Check if this is a new file (different from cached one)
        is_new_file = st.session_state.current_file_name != uploaded_file.name
        
        if is_new_file:
            # Load Excel file into DataFrame
            df = pd.read_excel(uploaded_file)

            if df.empty:
                st.warning("The uploaded document appears to be empty.")
            else:
                st.success("Document loaded successfully!")
                
                # Show column information
                st.subheader("Data Preview")
                st.dataframe(df.head(), use_container_width=True)
                
                # Show detected schema
                with st.expander("Detected Columns", expanded=False):
                    col_info = []
                    for col in df.columns:
                        dtype = str(df[col].dtype)
                        col_info.append(f"• **{col}** ({dtype})")
                    st.markdown("\n".join(col_info))

                # Only reinitialize if new file
                with st.spinner("Setting up AI agent for your data..."):
                    # Close previous connection if exists
                    if st.session_state.conn:
                        try:
                            st.session_state.conn.close()
                        except:
                            pass
                    
                    # Create unique database for this session
                    st.session_state.db_file = get_unique_db_name()
                    st.session_state.conn = create_connection(st.session_state.db_file)
                    load_excel_to_sql(df, st.session_state.conn)
                    
                    # Generate schema description from the actual DataFrame
                    schema_description = get_schema_from_dataframe(df)

                    # Set up LLM agent with SQL query tool and dynamic schema
                    st.session_state.chat_agent = setup_chat_agent(st.session_state.conn, schema_description)
                    
                    # Update current file name
                    st.session_state.current_file_name = uploaded_file.name
                
                st.success("✅ AI agent ready! You can now ask questions about your data.")
        else:
            # File already processed, just show the preview
            df = pd.read_excel(uploaded_file)
            st.success("Document loaded successfully!")
            
            # Show column information
            st.subheader("Data Preview")
            st.dataframe(df.head(), use_container_width=True)
            
            # Show detected schema
            with st.expander("Detected Columns", expanded=False):
                col_info = []
                for col in df.columns:
                    dtype = str(df[col].dtype)
                    col_info.append(f"• **{col}** ({dtype})")
                st.markdown("\n".join(col_info))

        # Question input field (only show if agent is ready)
        if st.session_state.chat_agent is not None:
            user_question = st.text_input(
                "Ask a question about your data:",
                placeholder="e.g., What is the total of column X? How many rows have Y > 100?"
            )

            if user_question:
                with st.spinner("Generating answer..."):
                    try:
                        answer = ask_question(st.session_state.chat_agent, user_question)
                        st.markdown("### Answer")
                        st.write(answer)
                    except Exception as e:
                        st.error(f"An error occurred while generating the response: {e}")
                        # Try to reconnect if connection issue
                        if "database" in str(e).lower():
                            st.info("Attempting to reconnect to database...")
                            try:
                                st.session_state.conn = create_connection(st.session_state.db_file)
                                df_reload = pd.read_excel(uploaded_file)
                                load_excel_to_sql(df_reload, st.session_state.conn)
                                schema_description = get_schema_from_dataframe(df_reload)
                                st.session_state.chat_agent = setup_chat_agent(st.session_state.conn, schema_description)
                                st.success("Reconnected! Please try your question again.")
                            except Exception as reconnect_error:
                                st.error(f"Reconnection failed: {reconnect_error}")

    except Exception as e:
        st.error(f"Failed to process the uploaded document: {e}")
else:
    st.info("Upload an Excel document to begin.")
    # Clear session state when no file is uploaded
    if st.session_state.conn:
        try:
            st.session_state.conn.close()
        except:
            pass
    st.session_state.chat_agent = None
    st.session_state.conn = None
    st.session_state.current_file_name = None
    st.session_state.db_file = None
