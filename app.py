import sqlite3
import os
import re
import pandas as pd
import sqlparse
import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

DB_PATH = "ecommerce.db"
MODEL_NAME = "gaussalgo/T5-LM-Large-text2sql-spider"

SCHEMA_CONTEXT = """
Tables:
- customers(customer_id, name, email, city, signup_date)
- products(product_id, name, category, price, stock)
- orders(order_id, customer_id, order_date, status, total_amount)
- order_items(item_id, order_id, product_id, quantity, unit_price)
"""

EXAMPLE_QUESTIONS = [
    "Show me all customers from San Jose",
    "What are the top 5 most expensive products?",
    "How many orders were completed?",
    "List products in the Electronics category",
    "What is the total revenue from completed orders?",
    "Which customers placed the most orders?",
    "Show all orders placed in 2024",
    "What is the average order amount by status?",
]

@st.cache_resource(show_spinner="Loading AI model...")
def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
    model.eval()
    return tokenizer, model

def generate_sql(question: str, tokenizer, model) -> str:
    prompt = f"{SCHEMA_CONTEXT.strip()} | {question}"
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=200,
            num_beams=4,
            early_stopping=True,
        )
    sql = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return sql.strip()

def clean_sql(sql: str) -> str:
    # Remove any trailing incomplete clause
    sql = re.sub(r"(WHERE|AND|OR|ORDER BY|GROUP BY|HAVING)\s*$", "", sql, flags=re.IGNORECASE).strip()
    sql = sql.rstrip(";").strip() + ";"
    return sql

def run_query(sql: str):
    if not os.path.exists(DB_PATH):
        from seed_db import seed
        seed()
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query(sql, conn)
        return df, None
    except Exception as e:
        return None, str(e)
    finally:
        conn.close()

def get_schema_info():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    tables = {}
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    for (table,) in cur.fetchall():
        cur.execute(f"PRAGMA table_info({table})")
        cols = [(row[1], row[2]) for row in cur.fetchall()]
        tables[table] = cols
    conn.close()
    return tables

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI SQL Query Generator",
    page_icon="🔍",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.hero {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border-radius: 16px;
    padding: 40px 48px;
    margin-bottom: 32px;
    color: white;
}
.hero h1 { font-size: 2.4rem; font-weight: 700; margin: 0 0 8px; }
.hero p  { font-size: 1.05rem; opacity: 0.8; margin: 0; }

.sql-box {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 18px 22px;
    font-family: 'Courier New', monospace;
    font-size: 0.95rem;
    color: #79c0ff;
    white-space: pre-wrap;
    word-break: break-word;
}

.badge {
    display: inline-block;
    background: #0f3460;
    color: #7dd3fc;
    border-radius: 20px;
    padding: 2px 12px;
    font-size: 0.78rem;
    font-weight: 600;
    margin: 2px;
}

.schema-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 10px;
}
.schema-card h4 { margin: 0 0 8px; color: #1e293b; font-size: 0.9rem; }

.metric-card {
    background: linear-gradient(135deg, #0f3460, #1a1a2e);
    border-radius: 12px;
    padding: 18px;
    color: white;
    text-align: center;
}
.metric-card .val { font-size: 1.8rem; font-weight: 700; }
.metric-card .lbl { font-size: 0.8rem; opacity: 0.7; margin-top: 4px; }
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🔍 AI SQL Query Generator</h1>
    <p>Ask questions in plain English — get SQL instantly. Powered by a free HuggingFace text-to-SQL model.</p>
</div>
""", unsafe_allow_html=True)

# ── Ensure DB exists ──────────────────────────────────────────────────────────
if not os.path.exists(DB_PATH):
    with st.spinner("Setting up sample e-commerce database..."):
        from seed_db import seed
        seed()

# ── Load model ────────────────────────────────────────────────────────────────
tokenizer, model = load_model()

# ── Layout ────────────────────────────────────────────────────────────────────
col_main, col_side = st.columns([2, 1], gap="large")

with col_main:
    st.markdown("### Ask a question")
    question = st.text_input(
        label="question",
        placeholder="e.g. What are the top 5 products by price?",
        label_visibility="collapsed",
    )

    st.markdown("**Try one of these:**")
    cols = st.columns(2)
    for i, example in enumerate(EXAMPLE_QUESTIONS):
        if cols[i % 2].button(example, key=f"ex_{i}", use_container_width=True):
            question = example

    st.markdown("---")

    if question:
        with st.spinner("Generating SQL..."):
            raw_sql = generate_sql(question, tokenizer, model)
            sql = clean_sql(raw_sql)
            formatted = sqlparse.format(sql, reindent=True, keyword_case="upper")

        st.markdown("### Generated SQL")
        st.markdown(f'<div class="sql-box">{formatted}</div>', unsafe_allow_html=True)

        copy_col, run_col = st.columns([1, 1])
        with run_col:
            run = st.button("▶ Run Query", type="primary", use_container_width=True)

        if run:
            with st.spinner("Running query..."):
                df, err = run_query(sql)

            if err:
                st.error(f"Query error: {err}")
                st.info("Tip: The AI model may occasionally produce imperfect SQL. Try rephrasing your question.")
            elif df is not None and not df.empty:
                st.markdown(f"### Results — {len(df)} row{'s' if len(df) != 1 else ''}")

                # Summary metrics
                m1, m2, m3 = st.columns(3)
                m1.markdown(f'<div class="metric-card"><div class="val">{len(df)}</div><div class="lbl">Rows</div></div>', unsafe_allow_html=True)
                m2.markdown(f'<div class="metric-card"><div class="val">{len(df.columns)}</div><div class="lbl">Columns</div></div>', unsafe_allow_html=True)
                numeric_cols = df.select_dtypes("number").columns
                if len(numeric_cols):
                    total = df[numeric_cols[0]].sum()
                    m3.markdown(f'<div class="metric-card"><div class="val">{total:,.1f}</div><div class="lbl">Sum of {numeric_cols[0]}</div></div>', unsafe_allow_html=True)
                else:
                    m3.markdown(f'<div class="metric-card"><div class="val">—</div><div class="lbl">No numeric col</div></div>', unsafe_allow_html=True)

                st.dataframe(df, use_container_width=True, height=350)

                csv = df.to_csv(index=False)
                st.download_button("⬇ Download CSV", csv, "results.csv", "text/csv")
            elif df is not None and df.empty:
                st.warning("Query ran successfully but returned no results.")

with col_side:
    st.markdown("### Database Schema")
    schema = get_schema_info()
    for table, cols in schema.items():
        col_tags = "".join(f'<span class="badge">{c} <span style="opacity:0.6">({t})</span></span>' for c, t in cols)
        st.markdown(f"""
        <div class="schema-card">
            <h4>📋 {table}</h4>
            {col_tags}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### How it works")
    st.markdown("""
    1. Your question + schema are sent to a **T5 text-to-SQL model**
    2. The model generates a **SQL query**
    3. The query runs on a local **SQLite e-commerce DB**
    4. Results are displayed as a table
    """)

    st.markdown("### Model")
    st.markdown("`gaussalgo/T5-LM-Large-text2sql-spider`")
    st.markdown("Free, runs locally — no API key needed.")
