# models/setup_db.py
import sqlite3
import os

# ساخت پوشه db اگر وجود نداشت
os.makedirs("db", exist_ok=True)

connection = sqlite3.connect("db/database.sqlite")
cursor = connection.cursor()
cursor.execute("DROP TABLE IF EXISTS menu_items")


# ایجاد جدول منو
cursor.execute("""
CREATE TABLE IF NOT EXISTS menu_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price INTEGER NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_details TEXT,
    total_price INTEGER,
    datetime TEXT
)
""")


# آیتم‌های اولیه
items = [
    ("BMT", "sandwich_15", 250),
    ("BMT", "sandwich_30", 450),
    ("Тунец", "sandwich_15", 240),
    ("Тунец", "sandwich_30", 430),
    ("Курица Терияки", "sandwich_15", 260),
    ("Курица Терияки", "sandwich_30", 460),
    ("Курица Барбекю", "sandwich_15", 270),
    ("Курица Барбекю", "sandwich_30", 470),
    ("Курица Грудка", "sandwich_15", 270),
    ("Курица Грудка", "sandwich_30", 470),
    ("Кофе Американо 200 мл", "drink", 150),
    ("Кофе Американо 400 мл", "drink", 250),
    ("Кофе Капучино 200 мл", "drink", 170),
    ("Кофе Капучино 400 мл", "drink", 270),
    ("Чай 200 мл", "drink", 70),
    ("Чай 400 мл", "drink", 90),
    ("Кофе Латте 200 мл", "drink", 180),
    ("Кофе Латте 400 мл", "drink", 280),
    ("Вода", "drink", 100),
    ("Цезарь с курицей", "salad", 350),
    ("Греческий салат", "salad", 300),
    ("Овощной салат", "salad", 280),
    ("Дополнительный сыр", "addons", 50),
    ("Дополнительное мясо", "addons", 100),
    ("Дополнительные овощи", "addons", 30),
]

cursor.executemany(
    "INSERT INTO menu_items (name, category, price) VALUES (?, ?, ?)", items)

connection.commit()
connection.close()
