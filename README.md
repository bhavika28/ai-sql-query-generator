# AI SQL Query Generator

> Ask questions in plain English — get SQL instantly. No API key required.

Built with a free HuggingFace text-to-SQL model (`gaussalgo/T5-LM-Large-text2sql-spider`), Streamlit, and a sample SQLite e-commerce database.

---

## Demo

| Ask | Get |
|-----|-----|
| "Show top 5 products by price" | `SELECT name, price FROM products ORDER BY price DESC LIMIT 5;` |
| "How many completed orders are there?" | `SELECT COUNT(*) FROM orders WHERE status = 'completed';` |
| "Total revenue by category" | `SELECT p.category, SUM(oi.quantity * oi.unit_price) FROM order_items oi JOIN products p ON oi.product_id = p.product_id GROUP BY p.category;` |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| AI Model | `gaussalgo/T5-LM-Large-text2sql-spider` (HuggingFace, free) |
| Database | SQLite (local e-commerce sample data) |
| Data | Pandas |
| SQL Formatting | sqlparse |
| ML Framework | PyTorch + HuggingFace Transformers |

---

## Project Structure

```
ai-sql-query-generator/
├── app.py            # Main Streamlit application
├── seed_db.py        # Seeds the sample SQLite e-commerce database
├── ecommerce.db      # Auto-generated on first run
├── requirements.txt  # Python dependencies
├── README.md
├── one-pager.md
└── slides.pptx
```

---

## Sample Database Schema

```
customers   (customer_id, name, email, city, signup_date)
products    (product_id, name, category, price, stock)
orders      (order_id, customer_id, order_date, status, total_amount)
order_items (item_id, order_id, product_id, quantity, unit_price)
```

50 customers · 25 products · 5 categories · 100+ orders with realistic data.

---

## Getting Started

### Prerequisites
- Python 3.9+
- ~2 GB disk space (for the T5-Large model download on first run)

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/bhavika28/ai-sql-query-generator.git
cd ai-sql-query-generator

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The database is seeded automatically on first launch. The HuggingFace model (~800 MB) downloads once and is cached locally.

---

## Example Questions to Try

- `Show me all customers from San Jose`
- `What are the top 5 most expensive products?`
- `How many orders were completed?`
- `List products in the Electronics category`
- `What is the total revenue from completed orders?`
- `Which customers placed the most orders?`
- `Show all orders placed in 2024`
- `What is the average order amount by status?`

---

## How It Works

```
User Question
     │
     ▼
Schema Context + Question  ──▶  T5 Text-to-SQL Model  ──▶  SQL Query
                                                                │
                                                                ▼
                                                     SQLite E-commerce DB
                                                                │
                                                                ▼
                                                      Results Table + CSV
```

1. The app prepends the database schema to your question as context
2. The T5 model generates a SQL query from the combined prompt
3. The query is cleaned, formatted, and executed on the local SQLite DB
4. Results are displayed as an interactive table with download option

---

## Roadmap

- [ ] Support custom database uploads (CSV → SQLite auto-conversion)
- [ ] Query history and saved favorites
- [ ] Multi-table JOIN suggestions
- [ ] Chart visualization of results
- [ ] Connect to PostgreSQL / MySQL

---

## Author

**Bhavika Prasannakumar**  
Data Scientist | [LinkedIn](https://linkedin.com/in/bhavikapk28) | [GitHub](https://github.com/bhavika28)
