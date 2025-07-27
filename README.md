# AI-Powered Excel Document QA Agent

A sophisticated Streamlit application that enables natural language querying of Excel documents using Google's Gemini LLM. Upload any Excel file and ask questions about your data in plain English - the AI will automatically understand your data structure and provide intelligent answers.

## 🌟 Features

- **Universal Excel Support**: Works with any Excel file format (.xlsx, .xls)
- **Dynamic Schema Detection**: Automatically identifies column names and data types
- **Natural Language Queries**: Ask questions in plain English about your data
- **Intelligent SQL Generation**: AI converts questions to optimized SQL queries
- **Smart Result Interpretation**: Returns human-readable answers, not raw SQL
- **Real-time Data Preview**: View your uploaded data and detected schema
- **Error Handling**: Robust error management for various edge cases

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd steward-titles
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

4. **Run the application**
   ```bash
   streamlit run main.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8501`

## 📊 Usage

### Step 1: Upload Your Excel File
- Click "Upload an Excel document"
- Select any `.xlsx` or `.xls` file
- The app will automatically detect columns and data types

### Step 2: Preview Your Data
- View the first few rows of your data
- Check the "Detected Columns" section to see all available fields

### Step 3: Ask Questions
Ask natural language questions like:
- *"What is the total sales amount?"*
- *"How many unique customers are there?"*
- *"Show me the top 5 products by quantity"*
- *"What's the average order value for each region?"*

### Step 4: Get Intelligent Answers
The AI will:
- Generate appropriate SQL queries
- Execute them on your data
- Return results in clear, conversational language

## 🛠️ Technical Architecture

### Core Components

- **`main.py`**: Streamlit web interface and application logic
- **`database.py`**: SQLite database operations and schema detection
- **`llm_agent.py`**: Google Gemini integration and query processing

### Data Flow

1. Excel file → Pandas DataFrame
2. DataFrame → SQLite database + Schema extraction
3. User question → Gemini LLM
4. LLM → SQL query → Database
5. Query results → LLM interpretation → Natural language answer

## 📋 Requirements

```
streamlit>=1.28.0
pandas>=1.5.0
google-generativeai>=0.3.0
python-dotenv>=1.0.0
openpyxl>=3.1.0
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Your Google Gemini API key | Yes |

### Getting a Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file

## 💡 Example Queries

Depending on your Excel data, you can ask questions like:

**Sales Data:**
- *"What were the total sales in Q1?"*
- *"Which salesperson had the highest revenue?"*
- *"Show me monthly sales trends"*

**Inventory Data:**
- *"How many items are below minimum stock level?"*
- *"What's the total value of inventory?"*
- *"Which products need reordering?"*

**Customer Data:**
- *"How many customers signed up this month?"*
- *"What's the geographic distribution of customers?"*
- *"Who are our top 10 customers by spending?"*

## 🔒 Security & Privacy

- Data is processed locally using SQLite in-memory database
- No data is permanently stored on disk (except temp SQLite file)
- API calls to Gemini only include schema information and queries, not raw data
- Uploaded files are temporarily processed and not retained

## 🐛 Troubleshooting

### Common Issues

**"API Key not found"**
- Ensure your `.env` file exists and contains `GEMINI_API_KEY`
- Verify your API key is valid and active

**"Failed to process Excel file"**
- Check file format is `.xlsx` or `.xls`
- Ensure file is not corrupted or password-protected
- Verify file contains actual data (not empty)

**"Error generating response"**
- Check your internet connection
- Verify Gemini API key has sufficient quota
- Try rephrasing your question more clearly

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the excellent web framework
- [Google Gemini](https://ai.google.dev/) for powerful LLM capabilities
- [Pandas](https://pandas.pydata.org/) for data processing

## 📞 Support

For questions, issues, or feature requests, please:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the troubleshooting section above

---

**Made with ❤️ for better data accessibility** 