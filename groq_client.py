"""
Groq API client for SQL generation
"""

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """You are an expert SQL developer. Your ONLY job is to convert natural language into clean, optimized SQL queries.

Rules:
1. Output ONLY the SQL query — no explanations, no markdown fences, no commentary.
2. Use standard SQL syntax (ANSI SQL) unless specified otherwise.
3. Use clear formatting: uppercase keywords, proper indentation.
4. If a schema is provided, STRICTLY use the given table and column names.
5. If ambiguous, make reasonable assumptions and add a short SQL comment.
6. Add inline SQL comments (-- comment) only if necessary.
7. Never refuse — always generate the best possible SQL.

Multi-table rules:
8. If multiple tables exist, infer joins using common column names (e.g., customer_id, order_id).
9. Prefer INNER JOIN unless specified otherwise.
10. ALWAYS qualify columns with table aliases when multiple tables are used.
11. Use short aliases like c, o, p for readability.

Data type handling:
12. If a column name suggests date/time (e.g., contains 'date'), treat it as DATE.
13. CAST date columns when using functions like AVG, DATE_PART, etc.
14. Avoid applying aggregate functions directly on VARCHAR columns.

Best practices:
15. Use GROUP BY when aggregation is present.
16. Use ORDER BY when results imply ranking or sorting.
17. Use LIMIT when user asks for top/bottom results.

Output format:
-- Optional comment (only if needed)
SELECT ...
FROM ...
JOIN ...
WHERE ...
GROUP BY ...
ORDER BY ...
LIMIT ...;
"""


class GroqSQLGenerator:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("❌ GROQ_API_KEY not found. Please set it in your .env file.")

        self.client = Groq(api_key=api_key)
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.schema = None
        self.history = []

    def set_schema(self, schema: str):
        """Set schema for context-aware SQL generation."""
        self.schema = schema.strip()

    def clear(self):
        """Clear history and schema."""
        self.history = []
        self.schema = None

    def get_history(self) -> list:
        """Return query history."""
        return self.history

    def _build_system_prompt(self) -> str:
        """Inject schema into system prompt."""
        if self.schema:
            return SYSTEM_PROMPT + f"\n\nDatabase Schema:\n{self.schema}"
        return SYSTEM_PROMPT

    def _clean_sql_output(self, sql: str) -> str:
        """
        Clean unwanted formatting from model output.
        (Sometimes LLMs add ```sql ``` blocks)
        """
        sql = sql.strip()

        if sql.startswith("```"):
            sql = sql.replace("```sql", "").replace("```", "").strip()

        return sql

    def generate_sql(self, natural_language: str) -> dict:
        """Generate SQL from natural language."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._build_system_prompt()},
                    {"role": "user", "content": natural_language},
                ],
                temperature=0.1,
                max_tokens=1024,
            )

            raw_output = response.choices[0].message.content
            sql_output = self._clean_sql_output(raw_output)

            # Save history
            self.history.append({
                "input": natural_language,
                "sql": sql_output,
            })

            return {
                "success": True,
                "input": natural_language,
                "sql": sql_output,
                "model": response.model,
                "tokens": response.usage.total_tokens,
            }

        except Exception as e:
            return {
                "success": False,
                "input": natural_language,
                "sql": None,
                "error": str(e),
            }