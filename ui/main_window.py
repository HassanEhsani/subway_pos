import sqlite3
import datetime
from PyQt6.QtCore import QTimer, QDateTime


from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QScrollArea,
    QGridLayout, QHBoxLayout, QListWidget
)
from PyQt6.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Subway POS")
        self.resize(1000, 600)

        self.cart = []  # سبد خرید در حافظه

        # 📦 طراحی رابط کلی
        main_layout = QHBoxLayout()

        # 📋 منو سمت چپ
        menu_layout = QVBoxLayout()
        title = QLabel("🟩 Меню")
        menu_layout.addWidget(title)

        # دکمه‌های دسته‌بندی
        btn_15 = QPushButton("Сэндвич 15 см")
        btn_30 = QPushButton("Сэндвич 30 см")
        btn_drink = QPushButton("Напитки")
        btn_salad = QPushButton("Салаты")
        btn_addons = QPushButton("Добавки")  # افزودنی‌ها

        # اتصال دکمه‌ها به دسته‌بندی
        btn_15.clicked.connect(lambda: self.load_items("sandwich_15"))
        btn_30.clicked.connect(lambda: self.load_items("sandwich_30"))
        btn_drink.clicked.connect(lambda: self.load_items("drink"))
        btn_salad.clicked.connect(lambda: self.load_items("salad"))
        btn_addons.clicked.connect(lambda: self.load_items("addons"))

        # دکمه‌ها در یک ردیف
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_15)
        btn_layout.addWidget(btn_30)
        btn_layout.addWidget(btn_drink)
        btn_layout.addWidget(btn_salad)
        btn_layout.addWidget(btn_addons)
        menu_layout.addLayout(btn_layout)
        
        

        # ناحیه اسکرول آیتم‌ها
        self.scroll = QScrollArea()
        self.menu_widget = QWidget()
        self.grid = QGridLayout()
        self.menu_widget.setLayout(self.grid)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.menu_widget)
        menu_layout.addWidget(self.scroll)

        main_layout.addLayout(menu_layout, 2)

        # 🛒 سبد خرید
        self.cart_list = QListWidget()
        self.total_label = QLabel("Общая сумма: 0 ₽")
        self.total_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.btn_submit_order = QPushButton("Оформить заказ")
        self.btn_submit_order.clicked.connect(self.submit_order)

        cart_layout = QVBoxLayout()
        cart_layout.addWidget(QLabel("🛒 Корзина"))
        cart_layout.addWidget(self.cart_list)
        cart_layout.addWidget(self.total_label)
        cart_layout.addWidget(self.btn_submit_order)

        main_layout.addLayout(cart_layout, 1)
        # 🕒 لیبل نمایش زمان
        self.datetime_label = QLabel()
        self.datetime_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.datetime_label.setStyleSheet("font-size: 14px; color: gray; padding: 5px;")

        # اضافه به layout سبد خرید
        cart_layout.addWidget(self.datetime_label)

        # تایمر برای آپدیت ساعت هر ثانیه
        timer = QTimer(self)
        timer.timeout.connect(self.update_datetime)
        timer.start(1000)  # هر ۱۰۰۰ میلی‌ثانیه (۱ ثانیه)

        # نمایش اولیه زمان
        self.update_datetime()


        self.setLayout(main_layout)

        # بارگذاری آیتم‌های اولیه
        self.load_items("sandwich_15")

    def load_items(self, category):
        connection = sqlite3.connect("db/database.sqlite")
        cursor = connection.cursor()
        cursor.execute("SELECT name, price FROM menu_items WHERE category = ?", (category,))
        items = cursor.fetchall()
        connection.close()

        # پاک‌سازی آیتم‌های قبلی
        for i in reversed(range(self.grid.count())):
            self.grid.itemAt(i).widget().setParent(None)

        # افزودن دکمه برای هر آیتم
        row = col = 0
        for name, price in items:
            btn = QPushButton(f"{name}\n{price} ₽")
            btn.setFixedSize(180, 80)
            btn.clicked.connect(lambda checked, n=name, p=price: self.add_to_cart(n, p))
            self.grid.addWidget(btn, row, col)
            col += 1
            if col == 3:
                col = 0
                row += 1

    def add_to_cart(self, name, price):
        self.cart.append((name, price))
        self.cart_list.addItem(f"{name} - {price} ₽")
        self.update_total()

    def update_total(self):
        total = sum(price for _, price in self.cart)
        self.total_label.setText(f"Общая сумма: {total} ₽")

    def submit_order(self):
        if not self.cart:
            print("Корзина пустая!")
            return

        connection = sqlite3.connect("db/database.sqlite")
        cursor = connection.cursor()

        now = datetime.datetime.now()
        current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")

        order_details = ", ".join([f"{name} ({price} ₽)" for name, price in self.cart])
        total_price = sum(price for _, price in self.cart)

        cursor.execute("""
            INSERT INTO orders (order_details, total_price, datetime)
            VALUES (?, ?, ?)
        """, (order_details, total_price, current_datetime))

        connection.commit()
        connection.close()

        print("Заказ сохранён!")
        self.cart.clear()
        self.cart_list.clear()
        self.update_total()
    
    def update_datetime(self):
        now = QDateTime.currentDateTime()
        self.datetime_label.setText(now.toString("yyyy-MM-dd   HH:mm:ss"))

