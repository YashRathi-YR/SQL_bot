import streamlit as st
from groq_client import GroqSQLGenerator
from schema_from_csv import infer_schema_from_multiple
from sql_executor import execute_query
from sql_fixer import fix_sql  # NEW

st.set_page_config(page_title="AI SQL Generator", layout="wide")

st.title("📊 AI SQL Generator from CSV")

# Initialize generator
generator = GroqSQLGenerator()

# Upload multiple CSV files
uploaded_files = st.file_uploader(
    "Upload CSV files",
    type=["csv"],
    accept_multiple_files=True
)

if uploaded_files:
    # 🔹 Step 1: Schema + Tables
    schema, tables = infer_schema_from_multiple(uploaded_files)

    st.subheader("📌 Inferred Schema")
    st.code(schema)

    generator.set_schema(schema)

    # 🔹 Step 2: Preview tables
    st.subheader("👀 Data Preview")
    for name, df in tables.items():
        st.markdown(f"**{name}**")
        st.dataframe(df.head())

    # 🔹 Step 3: User query
    query = st.text_input("💬 Ask your query in plain English")

    if st.button("Generate SQL"):
        if not query:
            st.warning("⚠️ Please enter a query")
        else:
            with st.spinner("⏳ Generating SQL..."):
                result = generator.generate_sql(query)

            if result["success"]:
                sql = result["sql"]

                st.subheader("🧾 Generated SQL")
                st.code(sql, language="sql")

                # 🔹 Step 4: Execute SQL
                try:
                    output_df = execute_query(tables, sql)

                except Exception as e:
                    # 🔥 Auto-fix layer
                    fixed_sql = fix_sql(sql, str(e))

                    try:
                        output_df = execute_query(tables, fixed_sql)

                        st.warning("⚠️ Query auto-corrected")
                        st.subheader("🛠 Fixed SQL")
                        st.code(fixed_sql, language="sql")

                    except Exception as e2:
                        st.error(f"❌ Execution Error: {e2}")
                        output_df = None

                # 🔹 Step 5: Show result
                if output_df is not None:
                    st.subheader("📊 Query Result")
                    st.dataframe(output_df)

                    # 🔹 Download option
                    st.download_button(
                        "⬇ Download Result CSV",
                        output_df.to_csv(index=False),
                        file_name="query_result.csv",
                        mime="text/csv"
                    )

            else:
                st.error(f"❌ Error: {result['error']}")