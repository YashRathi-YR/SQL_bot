import streamlit as st
from groq_client import GroqSQLGenerator
from schema_from_csv import infer_schema_from_multiple
from sql_executor import execute_query
from sql_fixer import fix_sql

st.set_page_config(page_title="AI SQL Generator", layout="wide", initial_sidebar_state="expanded")

# ============================================================
# ELEGANT STYLING - Modern Gradient & Color Theme
# ============================================================
st.markdown("""
<style>
/* Root color variables - Modern gradient theme */
:root {
    --primary: #0F766E;
    --primary-light: #14B8A6;
    --secondary: #7C3AED;
    --accent: #EC4899;
    --bg-dark: #0F172A;
    --bg-light: #F8FAFC;
    --surface: #1E293B;
    --border: #CBD5E1;
}

/* Main container styling */
.block-container {
    padding-top: 2rem;
    padding-left: 2.5rem;
    padding-right: 2.5rem;
    background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
}

/* Custom header styling */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F766E 0%, #14B8A6 100%);
}

[data-testid="stSidebar"] [data-testid="stVerticalBlock"] > [style*="flex-direction"] {
    background: transparent;
}

/* Sidebar text styling */
.stSidebar .stMarkdown h2,
.stSidebar .stMarkdown p,
.stSidebar .stMarkdown label {
    color: white !important;
}

.stSidebar .stFileUploader label {
    color: white !important;
    font-weight: 600;
}

.stSidebar .stFileUploader p {
    color: rgba(255, 255, 255, 0.8) !important;
}

/* Title styling */
h1 {
    background: linear-gradient(135deg, #0F766E 0%, #7C3AED 50%, #EC4899 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 800;
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

/* Subheader styling */
h2 {
    color: #0F766E;
    font-weight: 700;
    font-size: 1.4rem;
    margin-top: 1.5rem;
    margin-bottom: 1rem;
}

h3 {
    color: #1E293B;
    font-weight: 600;
}

/* Button styling - Primary Action */
.stButton > button {
    background: linear-gradient(135deg, #0F766E 0%, #14B8A6 100%);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    padding: 0.75rem 2rem;
    font-size: 1rem;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 15px rgba(15, 118, 110, 0.3);
}

.stButton > button:hover {
    background: linear-gradient(135deg, #14B8A6 0%, #0F766E 100%);
    box-shadow: 0 8px 25px rgba(15, 118, 110, 0.4);
    transform: translateY(-2px);
}

.stButton > button:active {
    transform: translateY(0);
}

/* Download button styling */
.stDownloadButton > button {
    background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    padding: 0.75rem 2rem;
    box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3);
}

.stDownloadButton > button:hover {
    background: linear-gradient(135deg, #A855F7 0%, #7C3AED 100%);
    box-shadow: 0 8px 25px rgba(124, 58, 237, 0.4);
    transform: translateY(-2px);
}

/* Text area styling */
.stTextArea > div > div > textarea {
    border: 2px solid #CBD5E1 !important;
    border-radius: 10px !important;
    font-family: 'Fira Code', monospace !important;
    background-color: #FFFFFF !important;
    transition: all 0.3s ease;
}

.stTextArea > div > div > textarea:focus {
    border-color: #14B8A6 !important;
    box-shadow: 0 0 0 3px rgba(20, 184, 166, 0.1) !important;
}

/* Code block styling */
[data-testid="stCodeBlock"] {
    border-radius: 12px;
    border: 1px solid #E2E8F0;
    background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

/* Tabs styling */
.stTabs [data-baseweb="tab-list"] button {
    font-weight: 600;
    color: #64748B;
    border-radius: 8px;
    padding: 0.5rem 1.5rem;
    transition: all 0.3s ease;
}

.stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
    background: linear-gradient(135deg, #0F766E 0%, #14B8A6 100%);
    color: white;
    box-shadow: 0 4px 12px rgba(15, 118, 110, 0.2);
}

.stTabs [data-baseweb="tab-list"] button:hover:not([aria-selected="true"]) {
    background-color: rgba(20, 184, 166, 0.1);
    color: #0F766E;
}

/* Info box styling */
.stInfo, .stSuccess, .stWarning, .stError {
    border-radius: 10px;
    border-left: 4px solid;
    padding: 1rem;
    font-weight: 500;
}

.stSuccess {
    background: linear-gradient(90deg, rgba(20, 184, 166, 0.1) 0%, rgba(20, 184, 166, 0.05) 100%);
    border-left-color: #14B8A6;
    color: #0F766E;
}

.stInfo {
    background: linear-gradient(90deg, rgba(59, 130, 246, 0.1) 0%, rgba(59, 130, 246, 0.05) 100%);
    border-left-color: #3B82F6;
    color: #1E40AF;
}

.stWarning {
    background: linear-gradient(90deg, rgba(245, 158, 11, 0.1) 0%, rgba(245, 158, 11, 0.05) 100%);
    border-left-color: #F59E0B;
    color: #92400E;
}

.stError {
    background: linear-gradient(90deg, rgba(239, 68, 68, 0.1) 0%, rgba(239, 68, 68, 0.05) 100%);
    border-left-color: #EF4444;
    color: #7F1D1D;
}

/* Expander styling */
.streamlit-expanderHeader {
    background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
    border-radius: 10px;
    border: 1px solid #E2E8F0;
    padding: 1rem;
    font-weight: 600;
    color: #0F766E;
    transition: all 0.3s ease;
}

.streamlit-expanderHeader:hover {
    background: linear-gradient(135deg, #F1F5F9 0%, #E2E8F0 100%);
    border-color: #14B8A6;
    box-shadow: 0 4px 12px rgba(20, 184, 166, 0.1);
}

/* Dataframe styling */
[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    border: 1px solid #E2E8F0;
}

[data-testid="stDataFrame"] table {
    border-collapse: collapse;
}

[data-testid="stDataFrame"] thead {
    background: linear-gradient(135deg, #0F766E 0%, #14B8A6 100%);
}

[data-testid="stDataFrame"] thead th {
    color: white;
    font-weight: 700;
    padding: 1rem !important;
    border: none;
}

[data-testid="stDataFrame"] tbody tr:nth-child(even) {
    background-color: #F8FAFC;
}

[data-testid="stDataFrame"] tbody tr:hover {
    background-color: #F1F5F9;
}

[data-testid="stDataFrame"] tbody td {
    padding: 0.75rem 1rem;
    border-bottom: 1px solid #E2E8F0;
}

/* Horizontal divider styling */
hr {
    border: none;
    border-top: 2px solid;
    background: linear-gradient(90deg, transparent 0%, #CBD5E1 50%, transparent 100%);
}

/* Caption styling */
.stCaption {
    color: #64748B;
    font-size: 0.95rem;
    font-weight: 500;
    margin-bottom: 1rem;
}

/* Spinner styling */
.stSpinner {
    color: #14B8A6;
}

/* File uploader styling */
.stFileUploader {
    border-radius: 10px;
    border: 2px dashed #CBD5E1;
    padding: 1.5rem;
    transition: all 0.3s ease;
}

.stFileUploader:hover {
    border-color: #14B8A6;
    background-color: rgba(20, 184, 166, 0.05);
}

/* Column container styling */
[data-testid="stColumn"] {
    padding: 1.5rem;
    background: white;
    border-radius: 12px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    transition: all 0.3s ease;
}

[data-testid="stColumn"]:hover {
    border-color: #14B8A6;
    box-shadow: 0 4px 16px rgba(20, 184, 166, 0.1);
}

/* Responsive adjustments */
@media (max-width: 768px) {
    h1 {
        font-size: 2rem;
    }
    
    .block-container {
        padding-left: 1.5rem;
        padding-right: 1.5rem;
    }
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# PAGE CONFIG & STATE INITIALIZATION
# ============================================================
if "result_df" not in st.session_state:
    st.session_state["result_df"] = None

# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.markdown("""
<div style="text-align: center; padding: 1.5rem 0; border-bottom: 2px solid rgba(255, 255, 255, 0.2); margin-bottom: 1rem;">
    <h2 style="color: white; margin: 0; font-size: 1.3rem;">📂 Data Hub</h2>
    <p style="color: rgba(255, 255, 255, 0.8); margin: 0.5rem 0 0 0; font-size: 0.9rem;">Upload & Query</p>
</div>
""", unsafe_allow_html=True)

uploaded_files = st.sidebar.file_uploader(
    "Upload CSV files",
    type=["csv"],
    accept_multiple_files=True,
    help="Select one or more CSV files to analyze"
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="text-align: center; padding: 1rem; color: rgba(255, 255, 255, 0.7); font-size: 0.85rem; margin-top: 2rem;">
    <p>✨ <strong>AI SQL Generator</strong></p>
    <p style="font-size: 0.8rem; margin-top: 0.5rem;">Query your data with natural language</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# MAIN TITLE & DESCRIPTION
# ============================================================
st.markdown("""
<div style="margin-bottom: 2rem;">
    <p style="color: #64748B; font-size: 1.1rem; margin-bottom: 0.5rem; font-weight: 500;">Welcome to</p>
</div>
""", unsafe_allow_html=True)

st.title("📊 AI SQL Generator")
st.caption("🚀 Transform natural language into intelligent SQL queries · Powered by Groq")

# ============================================================
# MAIN APP LOGIC
# ============================================================
generator = GroqSQLGenerator()

if uploaded_files:
    
    # Infer schema
    schema, tables = infer_schema_from_multiple(uploaded_files)
    generator.set_schema(schema)
    
    # Create tabs
    tab1, tab2 = st.tabs(["💬 Query Workspace", "📊 Results"])

    # ============================================================
    # TAB 1: QUERY WORKSPACE
    # ============================================================
    with tab1:
        
        # Two-column layout: Schema and Query
        col1, col2 = st.columns([1, 1], gap="large")

        # LEFT COLUMN: SCHEMA
        with col1:
            st.subheader("📁 Database Schema")
            st.markdown("""
            <div style="background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%); 
                        border-radius: 12px; padding: 1.5rem; border: 1px solid #E2E8F0;
                        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);">
            """, unsafe_allow_html=True)
            st.code(schema, language="sql")
            st.markdown("</div>", unsafe_allow_html=True)

        # RIGHT COLUMN: QUERY INPUT
        with col2:
            st.subheader("💬 Ask Your Question")
            
            query = st.text_area(
                "Natural language query",
                placeholder="e.g., Show me the top 5 customers by total spending\nor Find all transactions over $1000 from the past month",
                height=140,
                label_visibility="collapsed"
            )

            # Action buttons
            col_btn1, col_btn2 = st.columns([2, 1])
            with col_btn1:
                run_btn = st.button("🚀 Generate & Execute", use_container_width=True)
            with col_btn2:
                st.caption("Or press Ctrl+Enter")

        st.markdown("---")

        # Data preview section
        with st.expander("👀 Preview Data Tables", expanded=False):
            st.markdown("""
            <p style="color: #64748B; font-size: 0.9rem; margin-bottom: 1rem;">
            📋 Showing first 5 rows from each table
            </p>
            """, unsafe_allow_html=True)
            
            for name, df in tables.items():
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
                            border-radius: 8px; padding: 0.75rem 1rem; margin-bottom: 1rem;
                            border-left: 4px solid #14B8A6;">
                    <strong style="color: #0F766E;">📊 {name}</strong>
                </div>
                """, unsafe_allow_html=True)
                st.dataframe(df.head(), use_container_width=True)

        # ============================================================
        # QUERY EXECUTION SECTION
        # ============================================================
        if run_btn:

            if not query.strip():
                st.warning("⚠️ Please enter a query to get started")

            else:
                # Generate SQL
                with st.spinner("🔮 Generating SQL from your query..."):
                    result = generator.generate_sql(query)

                if result["success"]:
                    sql = result["sql"]

                    # Display generated SQL
                    st.markdown("### 🧾 Generated SQL")
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
                                border-radius: 12px; padding: 1.5rem; border: 1px solid #E2E8F0;
                                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);">
                    """, unsafe_allow_html=True)
                    st.code(sql, language="sql")
                    st.markdown("</div>", unsafe_allow_html=True)

                    # Try to execute query
                    try:
                        with st.spinner("⚡ Executing query..."):
                            output_df = execute_query(tables, sql)

                    except Exception as e:
                        st.warning("🔧 Auto-correcting SQL...")
                        
                        # Try to fix SQL
                        fixed_sql = fix_sql(sql, str(e))

                        try:
                            with st.spinner("⚡ Executing corrected query..."):
                                output_df = execute_query(tables, fixed_sql)

                            st.warning("⚠️ Query was auto-corrected and executed")
                            st.markdown("### 🧾 Corrected SQL")
                            st.markdown("""
                            <div style="background: linear-gradient(135deg, #FFF3CD 0%, #FFF8E1 100%);
                                        border-radius: 12px; padding: 1.5rem; border: 1px solid #FFE69C;
                                        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);">
                            """, unsafe_allow_html=True)
                            st.code(fixed_sql, language="sql")
                            st.markdown("</div>", unsafe_allow_html=True)

                        except Exception as e2:
                            st.error(f"❌ Execution failed: {str(e2)[:200]}")
                            output_df = None

                    # Store result and show success
                    if output_df is not None:
                        st.session_state["result_df"] = output_df
                        st.success("✅ Query executed successfully! Check the Results tab →")

                else:
                    st.error(f"❌ SQL Generation Error: {result['error']}")

    # ============================================================
    # TAB 2: RESULTS
    # ============================================================
    with tab2:
        
        if st.session_state["result_df"] is None:
            st.info("📝 No results yet. Run a query from the Query Workspace tab to see results here.")
        
        else:
            st.subheader("📊 Query Results")
            
            result_df = st.session_state["result_df"]
            
            # Display metrics
            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                st.metric("Rows", len(result_df), delta=None)
            with col_m2:
                st.metric("Columns", len(result_df.columns), delta=None)
            with col_m3:
                st.metric("Data Points", len(result_df) * len(result_df.columns), delta=None)
            
            st.markdown("---")
            
            # Display dataframe
            st.dataframe(result_df, use_container_width=True)

            # Download section
            st.markdown("### 📥 Export Results")
            col_down1, col_down2 = st.columns([2, 1])
            
            with col_down1:
                csv_data = result_df.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download as CSV",
                    data=csv_data,
                    file_name="query_results.csv",
                    mime="text/csv",
                    use_container_width=True
                )

else:
    # Initial state - no files uploaded
    st.markdown("""
    <div style="text-align: center; padding: 3rem 2rem;">
        <h2 style="color: #0F766E; font-size: 2rem; margin-bottom: 1rem;">👈 Get Started</h2>
        <p style="color: #64748B; font-size: 1.1rem; margin-bottom: 2rem;">
            Upload CSV files from the sidebar to begin querying your data with AI
        </p>
        <div style="background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
                    border-radius: 12px; padding: 2rem; border: 2px dashed #CBD5E1;
                    max-width: 500px; margin: 0 auto;">
            <p style="color: #64748B; font-size: 0.95rem; line-height: 1.6;">
                <strong>✨ Features:</strong><br>
                • Natural language to SQL conversion<br>
                • Automatic query error fixing<br>
                • Real-time data preview<br>
                • CSV export support<br>
                • Multi-table support
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
