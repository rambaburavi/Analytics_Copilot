from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///data/sample.db")

with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY,
            name TEXT
        );
    """))

    conn.execute(text("""
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            revenue FLOAT,
            order_date DATE
        );
    """))

    conn.commit()

print("Database created successfully ✅")