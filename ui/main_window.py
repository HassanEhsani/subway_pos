# ui/main_window.py
import sqlite3
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QScrollArea,
    QGridLayout, QHBoxLayout, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Subway POS")
        self.resize(1000, 600)

        self.cart = []  # سبد خرید در حافظه

        # طراحی رابط
        main_layout = QHBoxLayout()

        # 📋 منو سمت چپ
        menu_layout = QVBoxLayout()
        title = QLabel("🟩 Меню")
        menu_layout.addWidget(title)

        self.scroll = QScrollArea()
        self.menu_widget = QWidget()
        self.grid = QGridLayout()
        self.menu_widget.setLayout(self.grid)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.menu_widget)

        menu_layout.addWidget(self.scroll)
        main_layout.addLayout(menu_layout, 2)

        # 🛒 سبد خرید سمت راست
        self.cart_list = QListWidget()
        self.total_label = QLabel("Общая сумма: 0 ₽")
        self.total_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        cart_layout = QVBoxLayout()
        cart_layout.addWidget(QLabel("🛒 Корзина"))
        cart_layout.addWidget(self.cart_list)
        cart_layout.addWidget(self.total_label)

        main_layout.addLayout(cart_layout, 1)

        self.setLayout(main_layout)

        # بارگذاری آیتم‌ها
        self.load_items("sandwich_15")

    def load_items(self, category):
        connection = sqlite3.connect("db/database.sqlite")
        cursor = connection.cursor()
        cursor.execute("SELECT name, price FROM menu_items WHERE category = ?", (category,))
        items = cursor.fetchall()
        connection.close()

        # پاک کردن قبلی‌ها
        for i in reversed(range(self.grid.count())):
            self.grid.itemAt(i).widget().setParent(None)

        # افزودن دکمه‌ها
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
