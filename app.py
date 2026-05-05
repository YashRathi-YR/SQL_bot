import streamlit as st
from groq_client import GroqSQLGenerator
from schema_from_csv import infer_schema_from_csv
from sql_executor import execute_query

st.set_page_config(page_title="AI SQL Generator", layout="wide")

st.title("📊 AI SQL Generator from CSV")

generator = GroqSQLGenerator()

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    schema, df = infer_schema_from_csv(uploaded_file)

    st.subheader("📌 Inferred Schema")
    st.code(schema)

    generator.set_schema(schema)

    st.subheader("👀 Data Preview")
    st.dataframe(df.head())

    query = st.text_input("Ask your query in plain English")

    if st.button("Generate SQL"):
        if query:
            result = generator.generate_sql(query)

            if result["success"]:
                sql = result["sql"]

                st.subheader("🧾 Generated SQL")
                st.code(sql, language="sql")

                # Execute SQL
                try:
                    output_df = execute_query(df, sql)
                    st.subheader("📊 Query Result")
                    st.dataframe(output_df)

                    st.download_button(
                        "⬇ Download Result CSV",
                        output_df.to_csv(index=False),
                        file_name="result.csv"
                    )

                except Exception as e:
                    st.error(f"Execution Error: {e}")
            else:
                st.error(result["error"])