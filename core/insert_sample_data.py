import sqlite3

# Change this path if your DB file is elsewhere
DB_PATH = "data/sample.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Insert customers
cursor.execute("""
INSERT INTO customers (id, name) VALUES
(1, 'Alice'),
(2, 'Bob'),
(3, 'Charlie'),
(4, 'David'),
(5, 'Eva')
""")

# Insert orders
cursor.execute("""
INSERT INTO orders (id, customer_id, revenue) VALUES
(1, 1, 500),
(2, 1, 300),
(3, 2, 700),
(4, 3, 200),
(5, 4, 900),
(6, 5, 100)
""")

conn.commit()
conn.close()

print("Sample data inserted successfully!")