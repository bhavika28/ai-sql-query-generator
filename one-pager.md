# AI SQL Query Generator — Project One-Pager

**Author:** Bhavika Prasannakumar · Data Scientist  
**GitHub:** github.com/bhavika28/ai-sql-query-generator  
**Stack:** Python · Streamlit · HuggingFace T5 · SQLite · Pandas

---

## What Is It?

A web app that converts plain English questions into SQL queries using a free, locally-running AI model — no API key, no cost, no cloud dependency. Users type a question, get a SQL query, run it against a sample e-commerce database, and download the results.

---

## The Problem It Solves

Writing SQL requires technical knowledge most business users don't have. Analysts and managers with business questions are blocked behind engineers or BI tools. This app removes that barrier — if you can ask the question, you can get the data.

---

## How It Works

| Step | What Happens |
|------|-------------|
| 1 | User types a plain English question |
| 2 | App prepends the DB schema as context |
| 3 | T5-LM-Large (text2sql) model generates SQL |
| 4 | SQL runs against local SQLite e-commerce DB |
| 5 | Results shown as interactive table + CSV download |

---

## Key Features

- **No API key required** — runs entirely on local HuggingFace model
- **Sample e-commerce database** — 50 customers, 25 products, 100+ orders across 4 tables
- **One-click examples** — 8 pre-built questions to get started instantly
- **SQL formatting** — auto-formatted, readable output via sqlparse
- **Results export** — download any query result as CSV
- **Live schema viewer** — always-visible DB schema in the sidebar

---

## Tech Stack

```
Streamlit         →  Web UI
HuggingFace T5    →  Text-to-SQL AI model (gaussalgo/T5-LM-Large-text2sql-spider)
PyTorch           →  Model inference
SQLite            →  Sample database
Pandas            →  Data handling & display
sqlparse          →  SQL formatting
```

---

## Use Cases

- **Data Scientists** prototyping queries without writing SQL from scratch
- **Business Analysts** accessing data without engineering support
- **Students** learning SQL by seeing natural language mapped to queries
- **Demos** showcasing LLM-powered data tooling in interviews or portfolios

---

## Relevance to Bhavika's Background

This project directly extends skills from:
- **Lumen Technologies** — SQL pipelines, BI dashboards, LLM tooling, ERP chatbot
- **Brillio Technologies** — automated reporting, data visibility for stakeholders
- **Amazon Fraud Detection project** — NLP and text-based ML pipelines
- **MS in Applied Data Science** — ML Algorithms, NLP, Deep Learning coursework

---

## What's Next

- Upload any CSV → auto-convert to queryable DB
- Add chart/visualization layer on query results
- Extend to PostgreSQL / MySQL connections
- Deploy to Streamlit Cloud (free hosting)
