# 🗄️ SQL Code Generator — Powered by Groq

Convert plain English into production-ready SQL queries instantly using Groq's blazing-fast LLM inference.

---

## 🚀 Setup

### 1. Clone / Download the project
```bash
cd sql_generator
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure your API key
```bash
cp .env.example .env
# Edit .env and paste your Groq API key
```
Get your free API key at: https://console.groq.com

### 5. Run the app
```bash
python main.py
```

---

## 💬 Usage Examples

**No schema (generic SQL):**
```
You: Get all users who signed up in the last 30 days
```
```sql
SELECT *
FROM users
WHERE created_at >= CURRENT_DATE - INTERVAL '30 days';
```

**With schema:**
```
Schema description: Table: orders (id, customer_id, amount, status, created_at)
                    Table: customers (id, name, email, country)

You: Find top 5 customers by total order amount in 2024
```
```sql
SELECT
    c.name,
    c.email,
    SUM(o.amount) AS total_spent
FROM customers c
JOIN orders o ON c.id = o.customer_id
WHERE YEAR(o.created_at) = 2024
GROUP BY c.id, c.name, c.email
ORDER BY total_spent DESC
LIMIT 5;
```

---

## ⌨️ Commands

| Command | Description |
|---------|-------------|
| Type any English sentence | Generate SQL |
| `schema: <description>` | Update the database schema mid-session |
| `history` | View all past queries |
| `clear` | Reset schema and history |
| `exit` | Quit the app |

---

## 🛠️ Configuration

Edit `.env` to switch models:

| Model | Speed | Best For |
|-------|-------|----------|
| `llama-3.3-70b-versatile` | Fast | Complex queries (default) |
| `llama-3.1-8b-instant` | Fastest | Simple queries |
| `mixtral-8x7b-32768` | Fast | Long schema contexts |

---

## 📁 Project Structure

```
sql_generator/
├── main.py           # Entry point & CLI loop
├── groq_client.py    # Groq API wrapper & prompt logic
├── utils.py          # Display/formatting helpers
├── requirements.txt  # Dependencies
├── .env.example      # Config template
└── README.md
```
"# SQL_bot" 
