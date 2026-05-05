"""
SQL Code Generator using Groq API
Converts natural language queries to SQL code
"""

from groq_client import GroqSQLGenerator
from utils import print_banner, print_result, format_history


def main():
    print_banner()

    generator = GroqSQLGenerator()

    print("\n📋 Optionally describe your database schema for better results.")
    print("   (Press Enter to skip)\n")

    schema = input("Schema description: ").strip()
    if schema:
        generator.set_schema(schema)
        print("✅ Schema saved!\n")

    print("─" * 60)
    print("💬 Type your query in plain English. Commands:")
    print("   'history' - View past queries")
    print("   'clear'   - Clear schema/history")
    print("   'exit'    - Quit")
    print("─" * 60)

    while True:
        print()
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() == "exit":
            print("\n👋 Goodbye!\n")
            break

        elif user_input.lower() == "history":
            format_history(generator.get_history())
            continue

        elif user_input.lower() == "clear":
            generator.clear()
            print("🗑️  History and schema cleared.")
            continue

        elif user_input.lower().startswith("schema:"):
            new_schema = user_input[7:].strip()
            generator.set_schema(new_schema)
            print("✅ Schema updated!")
            continue

        print("\n⏳ Generating SQL...\n")
        result = generator.generate_sql(user_input)
        print_result(result)


if __name__ == "__main__":
    main()
