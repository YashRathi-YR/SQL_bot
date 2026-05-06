import streamlit as st
from groq_client import GroqSQLGenerator
from schema_from_csv import infer_schema_from_multiple
from sql_executor import execute_query
from sql_fixer import fix_sql

st.set_page_config(page_title="AI SQL Generator", layout="wide")

# -------------------------------
# Light Styling (subtle, not flashy)
# -------------------------------
# st.markdown("""
# <style>
# .block-container {
#     padding-top: 2rem;
# }
# [data-testid="stCodeBlock"] {
#     border-radius: 10px;
# }
# </style>
# """, unsafe_allow_html=True)

st.markdown("""
<style>
.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)
# -------------------------------
# Sidebar
# -------------------------------
st.sidebar.title("📂 Upload Data")
uploaded_files = st.sidebar.file_uploader(
    "Upload CSV files",
    type=["csv"],
    accept_multiple_files=True
)

st.sidebar.markdown("---")
st.sidebar.caption("AI SQL Generator")

# -------------------------------
# Title
# -------------------------------
st.title("📊 AI SQL Generator")
st.caption("Query your data using natural language")

generator = GroqSQLGenerator()

# -------------------------------
# Main App
# -------------------------------
if uploaded_files:

    schema, tables = infer_schema_from_multiple(uploaded_files)
    generator.set_schema(schema)

    # Tabs
    tab1, tab2 = st.tabs(["💬 Query Workspace", "📊 Results"])

    # -------------------------------
    # TAB 1 — MAIN WORKSPACE
    # -------------------------------
    with tab1:

        col1, col2 = st.columns([1, 1])

        # LEFT → Schema
        with col1:
            st.subheader("📁 Schema")
            st.code(schema)

        # RIGHT → Query Input
        with col2:
            st.subheader("💬 Ask Query")

            query = st.text_area(
                "Enter your query",
                placeholder="e.g. Show top 5 customers by total spending",
                height=120
            )

            run_btn = st.button("🚀 Run Query")

        st.markdown("---")

        # Data preview (collapsible)
        with st.expander("👀 Preview Tables"):
            for name, df in tables.items():
                st.markdown(f"**{name}**")
                st.dataframe(df.head())

        # SQL + Execution
        if run_btn:

            if not query:
                st.warning("⚠️ Please enter a query")

            else:
                with st.spinner("Generating SQL..."):
                    result = generator.generate_sql(query)

                if result["success"]:
                    sql = result["sql"]

                    st.subheader("🧾 Generated SQL")
                    st.code(sql, language="sql")

                    try:
                        output_df = execute_query(tables, sql)

                    except Exception as e:
                        fixed_sql = fix_sql(sql, str(e))

                        try:
                            output_df = execute_query(tables, fixed_sql)

                            st.warning("⚠️ Auto-corrected SQL")
                            st.code(fixed_sql, language="sql")

                        except Exception as e2:
                            st.error(f"❌ Execution Error: {e2}")
                            output_df = None

                    if output_df is not None:
                        st.session_state["result_df"] = output_df
                        st.success("✅ Query executed successfully")
                        st.info("👉 Check Results tab")

                else:
                    st.error(result["error"])

    # -------------------------------
    # TAB 2 — RESULTS
    # -------------------------------
    with tab2:
        if "result_df" not in st.session_state:
            st.info("No results yet. Run a query first.")
        else:
            st.subheader("📊 Query Results")
            st.dataframe(st.session_state["result_df"])

            st.download_button(
                "⬇ Download CSV",
                st.session_state["result_df"].to_csv(index=False),
                file_name="result.csv"
            )

else:
    st.info("👈 Upload CSV files from sidebar to begin")