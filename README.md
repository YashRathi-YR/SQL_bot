# 🧠 AI SQL Generator --- Powered by Groq

Convert natural language into **production-ready SQL queries** and
execute them instantly on your data.

✨ Built with **Streamlit + Groq LLM** for ultra-fast query generation.

------------------------------------------------------------------------

## 🚀 Features

-   🗣️ Natural Language → SQL
-   📂 Upload CSV files (auto schema detection)
-   ⚡ Execute queries instantly
-   🔧 Auto SQL error correction
-   📊 View results in table format
-   📥 Export results as CSV
-   🌙 Light / Dark mode support
-   🧩 Multi-table querying

------------------------------------------------------------------------

## 🖼️ Demo

![App UI](ui.png)
------------------------------------------------------------------------

## 🛠️ Setup

### 1. Clone the repository

``` bash
git clone <your-repo-url>
cd sql_generator
```

### 2. Create virtual environment

``` bash
python -m venv venv
```

#### Activate environment

``` bash
# macOS / Linux
source venv/bin/activate  

# Windows
venv\Scripts\activate
```

------------------------------------------------------------------------

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

### 4. Configure API Key

``` bash
copy .env.example .env   # Windows
cp .env.example .env     # macOS/Linux
```

Add your Groq API key inside `.env`:

    GROQ_API_KEY=your_api_key_here

Get your free API key: https://console.groq.com

------------------------------------------------------------------------

### 5. Run the Streamlit App

``` bash
streamlit run app.py

or 

python -m streamlit run app.py
```

App will open at:

    http://localhost:8501

------------------------------------------------------------------------

## 💬 Usage

1.  Upload CSV files from sidebar\
2.  Ask questions in plain English\
3.  SQL is generated automatically\
4.  Results displayed instantly\
5.  Download results as CSV

------------------------------------------------------------------------

## 🧪 Example Queries

-   Show top 5 customers by total spending\
-   Find total revenue by month\
-   Get customers from Mumbai\
-   Show all orders above 1000

------------------------------------------------------------------------

## ⚙️ Model Configuration

Edit `.env` to change model:

  Model                     Speed     Use Case
  ------------------------- --------- -----------------
  llama-3.3-70b-versatile   Fast      Complex queries
  llama-3.1-8b-instant      Fastest   Simple queries
  mixtral-8x7b-32768        Fast      Large schema

------------------------------------------------------------------------

sql_generator/
├── app.py                 # Streamlit UI (main app)
├── main.py                # Old CLI version (optional)
├── groq_client.py         # Groq API integration
├── schema_from_csv.py     # CSV → schema inference
├── sql_executor.py        # SQL execution engine
├── sql_fixer.py           # Auto SQL correction
├── utils.py               # Helper functions
├── requirements.txt
├── .env.example
└── README.md


------------------------------------------------------------------------
