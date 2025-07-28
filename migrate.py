import sqlite3

conn = sqlite3.connect("db/database.sqlite")
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE orders ADD COLUMN payment_method TEXT")
    print("✅ ستون payment_method اضافه شد.")
except sqlite3.OperationalError:
    print("⚠️ ستون payment_method از قبل وجود دارد.")

conn.commit()
conn.close()
