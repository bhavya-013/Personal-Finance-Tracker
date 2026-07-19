import sqlite3

conn = sqlite3.connect("finance.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    type TEXT,
    category TEXT,
    amount REAL,
    date TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS budgets(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    monthly_budget REAL
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS budgets(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE,
    monthly_budget REAL
)
""")
conn.commit()
conn.close()

print("Database Created Successfully")