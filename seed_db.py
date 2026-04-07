import sqlite3
import random
from datetime import datetime, timedelta

DB_PATH = "ecommerce.db"

def seed():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS customers;
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS orders;
        DROP TABLE IF EXISTS order_items;

        CREATE TABLE customers (
            customer_id   INTEGER PRIMARY KEY,
            name          TEXT NOT NULL,
            email         TEXT NOT NULL,
            city          TEXT NOT NULL,
            signup_date   TEXT NOT NULL
        );

        CREATE TABLE products (
            product_id    INTEGER PRIMARY KEY,
            name          TEXT NOT NULL,
            category      TEXT NOT NULL,
            price         REAL NOT NULL,
            stock         INTEGER NOT NULL
        );

        CREATE TABLE orders (
            order_id      INTEGER PRIMARY KEY,
            customer_id   INTEGER REFERENCES customers(customer_id),
            order_date    TEXT NOT NULL,
            status        TEXT NOT NULL,
            total_amount  REAL NOT NULL
        );

        CREATE TABLE order_items (
            item_id       INTEGER PRIMARY KEY,
            order_id      INTEGER REFERENCES orders(order_id),
            product_id    INTEGER REFERENCES products(product_id),
            quantity      INTEGER NOT NULL,
            unit_price    REAL NOT NULL
        );
    """)

    cities = ["San Jose", "Los Angeles", "New York", "Chicago", "Houston", "Seattle"]
    customers = [
        (i, f"Customer {i}", f"user{i}@email.com", random.choice(cities),
         (datetime(2022, 1, 1) + timedelta(days=random.randint(0, 900))).strftime("%Y-%m-%d"))
        for i in range(1, 51)
    ]
    cur.executemany("INSERT INTO customers VALUES (?,?,?,?,?)", customers)

    categories = ["Electronics", "Clothing", "Books", "Home", "Sports"]
    product_names = {
        "Electronics": ["Laptop", "Phone", "Tablet", "Headphones", "Smartwatch"],
        "Clothing":    ["T-Shirt", "Jeans", "Jacket", "Sneakers", "Dress"],
        "Books":       ["Python Basics", "ML Handbook", "Data Science 101", "AI Future", "SQL Mastery"],
        "Home":        ["Blender", "Coffee Maker", "Lamp", "Pillow", "Rug"],
        "Sports":      ["Yoga Mat", "Dumbbells", "Running Shoes", "Bicycle", "Tennis Racket"],
    }
    products = []
    pid = 1
    for cat, names in product_names.items():
        for name in names:
            products.append((pid, name, cat, round(random.uniform(10, 500), 2), random.randint(0, 200)))
            pid += 1
    cur.executemany("INSERT INTO products VALUES (?,?,?,?,?)", products)

    statuses = ["completed", "pending", "cancelled", "refunded"]
    orders = []
    order_items = []
    oid = 1
    iid = 1
    for cid in range(1, 51):
        for _ in range(random.randint(1, 6)):
            date = (datetime(2023, 1, 1) + timedelta(days=random.randint(0, 730))).strftime("%Y-%m-%d")
            status = random.choice(statuses)
            items_for_order = random.sample(products, random.randint(1, 4))
            total = 0.0
            for prod in items_for_order:
                qty = random.randint(1, 3)
                price = prod[3]
                total += qty * price
                order_items.append((iid, oid, prod[0], qty, price))
                iid += 1
            orders.append((oid, cid, date, status, round(total, 2)))
            oid += 1

    cur.executemany("INSERT INTO orders VALUES (?,?,?,?,?)", orders)
    cur.executemany("INSERT INTO order_items VALUES (?,?,?,?,?)", order_items)

    conn.commit()
    conn.close()
    print(f"Database seeded: {DB_PATH}")

if __name__ == "__main__":
    seed()
