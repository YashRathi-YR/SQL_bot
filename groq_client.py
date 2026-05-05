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
2. Use standard SQL syntax (ANSI SQL) unless the user specifies a dialect (MySQL, PostgreSQL, SQLite, etc.).
3. Use clear formatting: uppercase keywords (SELECT, FROM, WHERE), proper indentation.
4. If a schema is provided, use the exact table/column names from it.
5. If the request is ambiguous, make reasonable assumptions and add a brief comment above the SQL.
6. For complex queries, add inline SQL comments (-- comment) to explain key parts.
7. Never refuse a SQL generation request — always produce the best possible query.

Output format:
-- Optional: brief assumption note (only if truly ambiguous)
SELECT ...
FROM ...
WHERE ...;
"""


class GroqSQLGenerator:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError(
                "❌ GROQ_API_KEY not found. Please set it in your .env file."
            )

        self.client = Groq(api_key=api_key)
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.schema = None
        self.history = []

    def set_schema(self, schema: str):
        """Set the database schema for context-aware generation."""
        self.schema = schema.strip()

    def clear(self):
        """Clear history and schema."""
        self.history = []
        self.schema = None

    def get_history(self) -> list:
        """Return the query history."""
        return self.history

    def _build_system_prompt(self) -> str:
        """Build system prompt, injecting schema if available."""
        if self.schema:
            return (
                SYSTEM_PROMPT
                + f"\n\nDatabase Schema:\n{self.schema}"
            )
        return SYSTEM_PROMPT

    def generate_sql(self, natural_language: str) -> dict:
        """
        Convert natural language to SQL.

        Returns:
            dict with keys: 'sql', 'input', 'success', 'error'
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._build_system_prompt()},
                    {"role": "user", "content": natural_language},
                ],
                temperature=0.1,       # Low temp for deterministic SQL
                max_tokens=1024,
            )

            sql_output = response.choices[0].message.content.strip()

            # Save to history
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
