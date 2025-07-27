# models/setup_db.py
import sqlite3
import os

# ساخت پوشه db اگر وجود نداشت
os.makedirs("db", exist_ok=True)

connection = sqlite3.connect("db/database.sqlite")
cursor = connection.cursor()

# ایجاد جدول منو
cursor.execute("""
CREATE TABLE IF NOT EXISTS menu_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price INTEGER NOT NULL
)
""")

# آیتم‌های اولیه
items = [
    ("BMT", "sandwich_15", 250),
    ("BMT", "sandwich_30", 450),
    ("NUNNEC", "sandwich_15", 240),
    ("NUNNEC", "sandwich_30", 430),
    ("Курица Терияки", "sandwich_15", 260),
    ("Курица Терияки", "sandwich_30", 460),
    ("Курица Барбекю", "sandwich_15", 270),
    ("Курица Барбекю", "sandwich_30", 470),
    ("Вода", "drink", 100),
    ("Кофе Американо", "drink", 150),
    ("Кофе Капучино", "drink", 170),
    ("Кофе Латте", "drink", 180),
]

cursor.executemany("INSERT INTO menu_items (name, category, price) VALUES (?, ?, ?)", items)

connection.commit()
connection.close()
