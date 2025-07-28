import sqlite3
import datetime
import qtawesome as qta
from PyQt6.QtWidgets import QMessageBox, QInputDialog
from PyQt6.QtCore import QSize
from PyQt6.QtCore import QTimer, QDateTime
from PyQt6.QtWidgets import QMessageBox

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
        btn_15.setIcon(qta.icon("fa5s.bread-slice"))
        btn_15.setIconSize(QSize(24, 24))
        
        btn_30 = QPushButton("Сэндвич 30 см")
        btn_30.setIcon(qta.icon("fa5s.bread-slice"))
        btn_30.setIconSize(QSize(24, 24))
        
        btn_drink = QPushButton("Напитки")
        btn_drink.setIcon(qta.icon("fa5s.cocktail"))
        btn_drink.setIconSize(QSize(24, 24))

        btn_salad = QPushButton("Салаты")
        btn_salad.setIcon(qta.icon("fa5s.carrot"))
        btn_salad.setIconSize(QSize(24, 24))
        
        btn_addons = QPushButton("Добавки") 
        btn_addons.setIcon(qta.icon("fa5s.plus-circle"))
        btn_addons.setIconSize(QSize(24, 24))

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
        ##remove order

        self.total_label = QLabel("Общая сумма: 0 ₽")
        self.total_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.btn_submit_order = QPushButton("Оформить заказ")
        self.btn_submit_order.clicked.connect(self.submit_order)
        
        self.discount_button = QPushButton("Применить скидку")
        self.discount_button.clicked.connect(self.apply_discount)


        cart_layout = QVBoxLayout()
        cart_layout.addWidget(self.discount_button)
        cart_layout.addWidget(QLabel("🛒 Корзина"))
        cart_layout.addWidget(self.cart_list)
        cart_layout.addWidget(self.total_label)
        cart_layout.addWidget(self.btn_submit_order)
        
        ## order remove
        self.btn_remove_item = QPushButton("🗑 Удалить товар")
        self.btn_remove_item.clicked.connect(self.remove_selected_item)
        cart_layout.addWidget(self.btn_remove_item)


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
            QMessageBox.warning(self, "Ошибка", "Корзина пустая!")
            return

        # انتخاب روش پرداخت
        payment_method, ok = QInputDialog.getItem(
            self,
            "Выберите способ оплаты",
            "Способ оплаты:",
            ["Наличные", "Картой"],
            0,
            False
        )

        if not ok:
            return  # اگر کاربر انتخاب نکرد، خروج

        connection = sqlite3.connect("db/database.sqlite")
        cursor = connection.cursor()

        now = datetime.datetime.now()
        current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")

        order_details = ", ".join([f"{name} ({price} ₽)" for name, price in self.cart])
        total_price = self.discounted_total if hasattr(self, 'discount_applied') and self.discount_applied else sum(price for _, price in self.cart)

        try:
            cursor.execute("""
                INSERT INTO orders (order_details, total_price, datetime, payment_method)
                VALUES (?, ?, ?, ?)
            """, (order_details, total_price, current_datetime, payment_method))
            connection.commit()
            QMessageBox.information(self, "Успешно", "Заказ оформлен и сохранён.")
        except sqlite3.OperationalError as e:
            QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при сохранении заказа: {str(e)}")
        finally:
            connection.close()

        # ریست وضعیت
        self.discount_applied = False
        self.discounted_total = 0
        self.cart.clear()
        self.cart_list.clear()
        self.update_total()

    
    def update_datetime(self):
        now = QDateTime.currentDateTime()
        self.datetime_label.setText(now.toString("yyyy-MM-dd   HH:mm:ss"))
        
    def apply_discount(self):
        if not self.cart:
            return  # اگه سبد خالی بود هیچ کاری نکن

        discount_percent = 10  # مثلاً ۱۰٪ تخفیف بده
        original_total = sum(price for _, price in self.cart)
        discounted_total = int(original_total * (1 - discount_percent / 100))

        self.total_label.setText(f"Общая сумма со скидкой ({discount_percent}%): {discounted_total} ₽")

        # آپدیت لیست خرید هم انجام می‌دیم تا بعداً درست ذخیره شه
        self.discounted_total = discounted_total
        self.discount_applied = True
        
    # انتخاب روش پرداخت
        payment_method, ok = QInputDialog.getItem(
            self,
            "Выберите способ оплаты",
            "Способ оплаты:",
            ["Наличные", "Картой"],
            0,
            False
        )

        if not ok:
            return  # اگر کاربر انتخاب نکرد، خروج

        # سپس در دستور INSERT اینو اضافه کن:
        cursor.execute("""
            INSERT INTO orders (order_details, total_price, datetime, payment_method)
            VALUES (?, ?, ?, ?)
        """, (order_details, total_price, current_datetime, payment_method))

    
    ### remove order

    def remove_selected_item(self):
        selected_item = self.cart_list.currentItem()
        if selected_item is None:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите товар для удаления.")
            return

        reply = QMessageBox.question(
            self,
            "Подтверждение",
            f"Вы уверены, что хотите удалить '{selected_item.text()}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            row = self.cart_list.row(selected_item)
            if row >= 0:
                self.cart.pop(row)
                self.cart_list.takeItem(row)
                self.update_total()




