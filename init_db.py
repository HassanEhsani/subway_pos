import sqlite3

# اتصال به دیتابیس
conn = sqlite3.connect("db/database.sqlite")
cursor = conn.cursor()

# ساخت جدول سفارش‌ها
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_details TEXT,
    total_price INTEGER,
    datetime TEXT,
    payment_method TEXT DEFAULT 'unknown'
)
""")

print("✅ جدول orders با موفقیت ساخته شد.")

# بستن ارتباط
conn.commit()
conn.close()
