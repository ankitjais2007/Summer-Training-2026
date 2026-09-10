from tkinter import *
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from datetime import datetime
import os
import sys
import sqlite3


class Database:
    """SQLite database layer with integrity constraints."""

    def __init__(self, db_name="supermarket.db"):
        self.db_path = os.path.join(os.getcwd(), db_name)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.create_tables()

    def create_tables(self):
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                mobile TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL
                    CHECK (instr(email, '@') > 1 AND instr(email, '.') > 0)
            );

            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                subcategory TEXT NOT NULL,
                product_name TEXT NOT NULL,
                price REAL NOT NULL CHECK (price >= 0),
                stock INTEGER NOT NULL DEFAULT 100 CHECK (stock >= 0),
                UNIQUE(category, subcategory, product_name)
            );

            CREATE TABLE IF NOT EXISTS bills (
                bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
                bill_number TEXT NOT NULL UNIQUE,
                customer_id INTEGER NOT NULL,
                bill_date TEXT NOT NULL,
                subtotal REAL NOT NULL CHECK (subtotal >= 0),
                tax REAL NOT NULL CHECK (tax >= 0),
                total REAL NOT NULL CHECK (total >= 0),
                bill_text TEXT NOT NULL,
                FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
                    ON UPDATE CASCADE ON DELETE RESTRICT
            );

            CREATE TABLE IF NOT EXISTS bill_items (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                bill_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL CHECK (quantity > 0),
                price REAL NOT NULL CHECK (price >= 0),
                amount REAL NOT NULL CHECK (amount >= 0),
                FOREIGN KEY(bill_id) REFERENCES bills(bill_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY(product_id) REFERENCES products(product_id)
                    ON UPDATE CASCADE ON DELETE RESTRICT
            );
        """)
        self.conn.commit()

    def seed_products(self, products):
        for category, subcats in products.items():
            for subcategory, items in subcats.items():
                for product_name, price in items.items():
                    self.conn.execute("""
                        INSERT OR IGNORE INTO products
                        (category, subcategory, product_name, price, stock)
                        VALUES (?, ?, ?, ?, 100)
                    """, (category, subcategory, product_name, price))
        self.conn.commit()

    def close(self):
        self.conn.close()


class Billing_App:
    def __init__(self, root):

        self.root = root
        self.root.geometry("1530x800+0+0")
        self.root.title(" SUPERMARKET BILLING SOFTWARE")

        # ==========================================================
        # PRODUCT DATA
        # ==========================================================

        self.products = {
            "Clothing": {
                "Pant": {
                    "Levis": 5000,
                    "Mufti": 7000,
                    "Spykar": 8000
                },
                "T-Shirt": {
                    "Polo": 1500,
                    "Roadster": 1800,
                    "Jack&Jones": 1700
                },
                "Shirt": {
                    "Peter England": 2100,
                    "Louis Phillipe": 2700,
                    "Park Avenue": 1740
                }
            },

            "LifeStyle": {
                "Bath Soap": {
                    "LifeBuy": 20,
                    "Lux": 20,
                    "Santoor": 20,
                    "Pearl": 30
                },
                "Face Creame": {
                    "Fair&Lovely": 20,
                    "Ponds": 20,
                    "Olay": 20,
                    "Garnier": 30
                },
                "Hair Oil": {
                    "Parachute": 25,
                    "Jashmin": 22,
                    "Bajaj": 30
                }
            },

            "Mobiles": {
                "Iphone": {
                    "Iphone_X": 40000,
                    "Iphone_11": 60000,
                    "Iphone_12": 85000
                },
                "Sumsung": {
                    "Samsung M16": 16000,
                    "Sumsung M12": 12000,
                    "Samsung M21": 18000
                },
                "Xiome": {
                    "Red11": 11000,
                    "Redme-12": 12000,
                    "RedmePro": 9000
                },
                "RealMe": {
                    "RealMe 12": 25000,
                    "RealMe 13": 22000,
                    "RealMe Pro": 30000
                },
                "One+": {
                    "OnePlus1": 45000,
                    "OnePlus2": 60000,
                    "OnePlus3": 45800
                }
            }
        }

        self.Category = [
            "Select Option",
            "Clothing",
            "LifeStyle",
            "Mobiles"
        ]

        # Cart and bill settings
        self.cart = []
        self.tax_rate = 5.0
        self.bill_number = self.create_bill_number()

        # Create bill folder automatically
        self.bill_folder = os.path.join(os.getcwd(), "bills")
        os.makedirs(self.bill_folder, exist_ok=True)

        # SQLite database
        self.db = Database()
        self.db.seed_products(self.products)
        self.bill_saved_to_db = False

        # ==========================================================
        # IMAGES
        # ==========================================================

        img1 = Image.open("images/img1.jpg")
        img1 = img1.resize((500, 130), Image.Resampling.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)

        lbl_img1 = Label(self.root, image=self.photoimg1)
        lbl_img1.place(x=0, y=0, width=500, height=130)

        img2 = Image.open("images/img2.jpg")
        img2 = img2.resize((500, 130), Image.Resampling.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)

        lbl_img2 = Label(self.root, image=self.photoimg2)
        lbl_img2.place(x=500, y=0, width=500, height=130)

        img3 = Image.open("images/img3.jpg")
        img3 = img3.resize((500, 130), Image.Resampling.LANCZOS)
        self.photoimg3 = ImageTk.PhotoImage(img3)

        lbl_img3 = Label(self.root, image=self.photoimg3)
        lbl_img3.place(x=1000, y=0, width=500, height=130)

        # ==========================================================
        # TITLE
        # ==========================================================

        lbl_title = Label(
            self.root,
            text="WELCOME TO JAISWAL SUPERMARKET",
            font=('times new roman', 30, "bold"),
            bg='white',
            fg='navy'
        )
        lbl_title.place(x=0, y=130, width=1530, height=42)

        # ==========================================================
        # MAIN FRAME
        # ==========================================================

        Main_Frame = Frame(
            self.root,
            bd=5,
            relief=GROOVE,
            bg='white'
        )
        Main_Frame.place(x=0, y=175, width=1530, height=605)

        # ==========================================================
        # CUSTOMER FRAME
        # ==========================================================

        Cust_Frame = LabelFrame(
            Main_Frame,
            text='Customer',
            font=('times new roman', 12, "bold"),
            bg='white',
            fg='red'
        )
        Cust_Frame.place(x=10, y=5, width=350, height=140)

        lbl_mob = Label(
            Cust_Frame,
            text="Mobile No.",
            font=('times new roman', 12, "bold"),
            bg='white'
        )
        lbl_mob.grid(row=0, column=0, sticky=W, padx=5, pady=2)

        self.entry_mob = ttk.Entry(
            Cust_Frame,
            font=('times new roman', 10, "bold"),
            width=25
        )
        self.entry_mob.grid(row=0, column=1, sticky=W, padx=5, pady=2)

        lbl_name = Label(
            Cust_Frame,
            text="Customer Name",
            font=('times new roman', 12, "bold"),
            bg='white'
        )
        lbl_name.grid(row=1, column=0, sticky=W, padx=5, pady=2)

        self.entry_name = ttk.Entry(
            Cust_Frame,
            font=('times new roman', 10, "bold"),
            width=25
        )
        self.entry_name.grid(row=1, column=1, sticky=W, padx=5, pady=2)

        lbl_email = Label(
            Cust_Frame,
            text="Email",
            font=('times new roman', 12, "bold"),
            bg='white'
        )
        lbl_email.grid(row=2, column=0, sticky=W, padx=5, pady=2)

        self.entry_email = ttk.Entry(
            Cust_Frame,
            font=('times new roman', 10, "bold"),
            width=25
        )
        self.entry_email.grid(row=2, column=1, sticky=W, padx=5, pady=2)

        # ==========================================================
        # PRODUCT FRAME
        # ==========================================================

        Product_Frame = LabelFrame(
            Main_Frame,
            text='Product',
            font=('times new roman', 12, "bold"),
            bg='white',
            fg='red'
        )
        Product_Frame.place(x=375, y=5, width=570, height=140)

        lbl_category = Label(
            Product_Frame,
            text="Select Category",
            font=('times new roman', 12, "bold"),
            bg='white'
        )
        lbl_category.grid(row=0, column=0, sticky=W, padx=5, pady=2)

        self.combo_category = ttk.Combobox(
            Product_Frame,
            values=self.Category,
            font=('times new roman', 10, "bold"),
            width=25,
            state='readonly'
        )
        self.combo_category.current(0)
        self.combo_category.grid(row=0, column=1, sticky=W, padx=5, pady=2)
        self.combo_category.bind("<<ComboboxSelected>>", self.Categories)

        lbl_Subcategory = Label(
            Product_Frame,
            text="Subcategory",
            font=('times new roman', 12, "bold"),
            bg='white'
        )
        lbl_Subcategory.grid(row=1, column=0, sticky=W, padx=5, pady=2)

        self.combo_Subcategory = ttk.Combobox(
            Product_Frame,
            font=('times new roman', 10, "bold"),
            width=25,
            state='readonly'
        )
        self.combo_Subcategory.grid(row=1, column=1, sticky=W, padx=5, pady=2)
        self.combo_Subcategory.bind("<<ComboboxSelected>>", self.SubCategories)

        lbl_ProductName = Label(
            Product_Frame,
            text="Product Name",
            font=('times new roman', 12, "bold"),
            bg='white'
        )
        lbl_ProductName.grid(row=2, column=0, sticky=W, padx=5, pady=2)

        self.combo_ProductName = ttk.Combobox(
            Product_Frame,
            font=('times new roman', 10, "bold"),
            width=25,
            state='readonly'
        )
        self.combo_ProductName.grid(row=2, column=1, sticky=W, padx=5, pady=2)
        self.combo_ProductName.bind("<<ComboboxSelected>>", self.ProductName)

        lbl_price = Label(
            Product_Frame,
            text="Price",
            font=('times new roman', 12, "bold"),
            bg='white'
        )
        lbl_price.grid(row=0, column=2, sticky=W, padx=5, pady=2)

        self.combo_price = ttk.Combobox(
            Product_Frame,
            font=('times new roman', 10, "bold"),
            width=20,
            state='readonly'
        )
        self.combo_price.grid(row=0, column=3, sticky=W, padx=5, pady=2)

        qty = Label(
            Product_Frame,
            text='Qty',
            font=("times new roman", 10, "bold"),
            bg='white'
        )
        qty.grid(row=1, column=2, sticky=W, padx=5, pady=2)

        self.entry_qty = ttk.Entry(
            Product_Frame,
            font=('times new roman', 10, "bold"),
            width=23
        )
        self.entry_qty.grid(row=1, column=3, sticky=W, padx=5, pady=2)

        # ==========================================================
        # BILL SEARCH
        # ==========================================================

        bill_number_label = ttk.Label(Main_Frame, text="Bill Number")
        bill_number_label.place(x=970, y=12)

        self.entry_search = ttk.Entry(
            Main_Frame,
            font=('times new roman', 10, "bold"),
            width=25
        )
        self.entry_search.place(x=1050, y=12)

        btn_search = Button(
            Main_Frame,
            width=10,
            text='Search',
            font=('arial', 10, "bold"),
            bg='green',
            fg='white',
            cursor='hand2',
            command=self.search_bill
        )
        btn_search.place(x=1250, y=10)

        # ==========================================================
        # BILL AREA
        # ==========================================================

        RightLabelFrame = LabelFrame(
            Main_Frame,
            text='Bill Area',
            font=('times new roman', 12, "bold"),
            bg='white',
            fg='red'
        )
        RightLabelFrame.place(x=1000, y=50, width=500, height=530)

        scroll_y = Scrollbar(RightLabelFrame, orient=VERTICAL)

        self.textarea = Text(
            RightLabelFrame,
            yscrollcommand=scroll_y.set,
            bg='white',
            fg='blue',
            font=('times new roman', 12, "bold")
        )

        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.textarea.yview)
        self.textarea.pack(fill=BOTH, expand=1)

        # ==========================================================
        # BILL COUNTER FRAME
        # ==========================================================

        BillCounterFrame = LabelFrame(
            Main_Frame,
            text='Bill Area',
            font=('times new roman', 12, "bold"),
            bg='white',
            fg='red'
        )
        BillCounterFrame.place(x=10, y=160, width=940, height=420)

        # Subtotal
        lbl_subtotal = Label(
            BillCounterFrame,
            text="Subtotal",
            font=('times new roman', 12, "bold"),
            bg='white'
        )
        lbl_subtotal.grid(row=0, column=0, sticky=W, padx=10, pady=20)

        self.entry_subtotal = ttk.Entry(
            BillCounterFrame,
            font=('times new roman', 10, "bold"),
            width=25
        )
        self.entry_subtotal.grid(row=0, column=1, sticky=W, padx=10, pady=20)

        # Tax
        lbl_tax = Label(
            BillCounterFrame,
            text="Gov Tax",
            font=('times new roman', 12, "bold"),
            bg='white'
        )
        lbl_tax.grid(row=1, column=0, sticky=W, padx=10, pady=20)

        self.entry_tax = ttk.Entry(
            BillCounterFrame,
            font=('times new roman', 10, "bold"),
            width=25
        )
        self.entry_tax.grid(row=1, column=1, sticky=W, padx=10, pady=20)

        # Total
        lbl_amoutTotal = Label(
            BillCounterFrame,
            text="Total",
            font=('times new roman', 12, "bold"),
            bg='white'
        )
        lbl_amoutTotal.grid(row=2, column=0, sticky=W, padx=10, pady=20)

        self.entry_amoutTotal = ttk.Entry(
            BillCounterFrame,
            font=('times new roman', 10, "bold"),
            width=25
        )
        self.entry_amoutTotal.grid(row=2, column=1, sticky=W, padx=10, pady=20)

        # ==========================================================
        # BUTTON FRAME
        # ==========================================================

        ButtonFrame = Frame(BillCounterFrame, bd=2, bg='white')
        ButtonFrame.place(x=350, y=20)

        addCart = Button(
            ButtonFrame,
            text='Add To Cart',
            font=('arial', 15, "bold"),
            bg='orangered',
            fg='white',
            cursor='hand2',
            command=self.add_to_cart
        )
        addCart.grid(row=0, column=0, padx=10, pady=10)

        generateBill = Button(
            ButtonFrame,
            text='Generate Bill',
            font=('arial', 15, "bold"),
            bg='orangered',
            fg='white',
            cursor='hand2',
            command=self.generate_bill
        )
        generateBill.grid(row=0, column=1, padx=10, pady=10)

        save = Button(
            ButtonFrame,
            width=10,
            text='Save Bill',
            font=('arial', 15, "bold"),
            bg='orangered',
            fg='white',
            cursor='hand2',
            command=self.save_bill
        )
        save.grid(row=0, column=2, padx=10, pady=10)

        printBill = Button(
            ButtonFrame,
            width=10,
            text='Print',
            font=('arial', 15, "bold"),
            bg='orangered',
            fg='white',
            cursor='hand2',
            command=self.print_bill
        )
        printBill.grid(row=1, column=0, padx=10, pady=10)

        clear = Button(
            ButtonFrame,
            width=11,
            text='Clear',
            font=('arial', 15, "bold"),
            bg='orangered',
            fg='white',
            cursor='hand2',
            command=self.clear_all
        )
        clear.grid(row=1, column=1, padx=10, pady=10)

        btn_exit = Button(
            ButtonFrame,
            width=10,
            text='Exit',
            font=('arial', 15, "bold"),
            bg='orangered',
            fg='white',
            cursor='hand2',
            command=self.exit_app
        )
        btn_exit.grid(row=1, column=2, padx=10, pady=10)

    # ==============================================================
    # BILL NUMBER
    # ==============================================================

    def create_bill_number(self):
        return datetime.now().strftime("%Y%m%d%H%M%S")

    # ==============================================================
    # CATEGORY -> SUBCATEGORY
    # ==============================================================

    def Categories(self, event=""):

        category = self.combo_category.get()

        self.combo_Subcategory.set("")
        self.combo_ProductName.set("")
        self.combo_price.set("")

        self.combo_Subcategory["values"] = ()
        self.combo_ProductName["values"] = ()
        self.combo_price["values"] = ()

        if category == "Select Option":
            return

        rows = self.db.conn.execute(
            "SELECT DISTINCT subcategory FROM products "
            "WHERE category = ? ORDER BY subcategory",
            (category,)
        ).fetchall()

        subcategories = [row[0] for row in rows]
        self.combo_Subcategory["values"] = subcategories

        if subcategories:
            self.combo_Subcategory.current(0)
            self.SubCategories()

    # ==============================================================
    # SUBCATEGORY -> PRODUCT
    # ==============================================================

    def SubCategories(self, event=""):

        category = self.combo_category.get()
        subcategory = self.combo_Subcategory.get()

        self.combo_ProductName.set("")
        self.combo_price.set("")

        self.combo_ProductName["values"] = ()
        self.combo_price["values"] = ()

        rows = self.db.conn.execute(
            "SELECT product_name FROM products "
            "WHERE category = ? AND subcategory = ? "
            "ORDER BY product_name",
            (category, subcategory)
        ).fetchall()

        products = [row[0] for row in rows]
        self.combo_ProductName["values"] = products

        if products:
            self.combo_ProductName.current(0)
            self.ProductName()

    # ==============================================================
    # PRODUCT -> PRICE
    # ==============================================================

    def ProductName(self, event=""):

        category = self.combo_category.get()
        subcategory = self.combo_Subcategory.get()
        product = self.combo_ProductName.get()

        row = self.db.conn.execute(
            "SELECT price FROM products "
            "WHERE category = ? AND subcategory = ? AND product_name = ?",
            (category, subcategory, product)
        ).fetchone()

        if row:
            price = row[0]
            self.combo_price["values"] = [price]
            self.combo_price.current(0)

    # ==============================================================
    # ADD TO CART
    # ==============================================================

    def add_to_cart(self):

        category = self.combo_category.get()
        subcategory = self.combo_Subcategory.get()
        product = self.combo_ProductName.get()
        qty_text = self.entry_qty.get().strip()

        if category == "Select Option" or not category:
            messagebox.showerror("Error", "Please select a category.")
            return
        if not subcategory:
            messagebox.showerror("Error", "Please select a subcategory.")
            return
        if not product:
            messagebox.showerror("Error", "Please select a product.")
            return
        if not qty_text:
            messagebox.showerror("Error", "Please enter quantity.")
            self.entry_qty.focus()
            return

        try:
            quantity = int(qty_text)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Invalid Quantity",
                "Quantity must be a positive whole number."
            )
            self.entry_qty.focus()
            return

        row = self.db.conn.execute(
            "SELECT product_id, price, stock FROM products "
            "WHERE category = ? AND subcategory = ? AND product_name = ?",
            (category, subcategory, product)
        ).fetchone()

        if not row:
            messagebox.showerror("Database Error", "Product was not found in database.")
            return

        product_id, price, stock = row

        # Include quantities of the same product already waiting in the cart.
        already_in_cart = sum(
            item["quantity"] for item in self.cart
            if item["product_id"] == product_id
        )

        if already_in_cart + quantity > stock:
            messagebox.showerror(
                "Insufficient Stock",
                f"Available stock for {product}: {stock}\n"
                f"Already in cart: {already_in_cart}\n"
                f"Requested now: {quantity}"
            )
            return

        amount = float(price) * quantity

        self.cart.append({
            "product_id": product_id,
            "category": category,
            "subcategory": subcategory,
            "product": product,
            "price": float(price),
            "quantity": quantity,
            "amount": amount
        })

        # Cart has changed, so a previous DB bill is no longer current.
        self.bill_saved_to_db = False

        messagebox.showinfo(
            "Added",
            f"{product} added to cart.\n"
            f"Quantity: {quantity}\n"
            f"Amount: ₹{amount:.2f}"
        )

        self.entry_qty.delete(0, END)
        self.update_totals()

    # ==============================================================
    # UPDATE TOTALS
    # ==============================================================

    def update_totals(self):

        subtotal = sum(item["amount"] for item in self.cart)

        tax = subtotal * self.tax_rate / 100
        total = subtotal + tax

        self.set_entry(self.entry_subtotal, f"{subtotal:.2f}")
        self.set_entry(self.entry_tax, f"{tax:.2f}")
        self.set_entry(self.entry_amoutTotal, f"{total:.2f}")

    # ==============================================================
    # GENERATE BILL
    # ==============================================================

    def generate_bill(self):

        if not self.validate_customer():
            return

        if not self.cart:
            messagebox.showerror(
                "Empty Cart",
                "Please add at least one product to the cart."
            )
            return

        if not self.save_bill_to_database():
            return

        bill = self.create_bill_text()

        self.textarea.delete("1.0", END)
        self.textarea.insert(END, bill)

        messagebox.showinfo(
            "Bill Generated",
            f"Bill #{self.bill_number} generated successfully."
        )

    # ==============================================================
    # SAVE BILL TO SQLITE - TRANSACTION
    # ==============================================================

    def save_bill_to_database(self):

        if self.bill_saved_to_db:
            return True

        subtotal = sum(item["amount"] for item in self.cart)
        tax = subtotal * self.tax_rate / 100
        total = subtotal + tax
        bill_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Build the exact bill text before saving it as a snapshot.
        bill_text = self.create_bill_text()

        conn = self.db.conn

        try:
            conn.execute("BEGIN")

            # Insert customer or update the existing customer's details.
            customer_row = conn.execute(
                "SELECT customer_id FROM customers WHERE mobile = ?",
                (self.entry_mob.get().strip(),)
            ).fetchone()

            if customer_row:
                customer_id = customer_row[0]
                conn.execute(
                    "UPDATE customers SET name = ?, email = ? "
                    "WHERE customer_id = ?",
                    (
                        self.entry_name.get().strip(),
                        self.entry_email.get().strip(),
                        customer_id
                    )
                )
            else:
                cursor = conn.execute(
                    "INSERT INTO customers(name, mobile, email) "
                    "VALUES (?, ?, ?)",
                    (
                        self.entry_name.get().strip(),
                        self.entry_mob.get().strip(),
                        self.entry_email.get().strip()
                    )
                )
                customer_id = cursor.lastrowid

            # Re-check stock inside the same transaction.
            for item in self.cart:
                row = conn.execute(
                    "SELECT stock, price FROM products WHERE product_id = ?",
                    (item["product_id"],)
                ).fetchone()

                if not row:
                    raise ValueError(
                        f"Product '{item['product']}' no longer exists."
                    )

                stock, db_price = row

                if stock < item["quantity"]:
                    raise ValueError(
                        f"Insufficient stock for '{item['product']}'. "
                        f"Available: {stock}, requested: {item['quantity']}."
                    )

                # Use the database price as the authoritative price.
                item["price"] = float(db_price)
                item["amount"] = item["price"] * item["quantity"]

            # Recalculate totals after the DB price check.
            subtotal = sum(item["amount"] for item in self.cart)
            tax = subtotal * self.tax_rate / 100
            total = subtotal + tax
            bill_text = self.create_bill_text()

            bill_cursor = conn.execute(
                "INSERT INTO bills "
                "(bill_number, customer_id, bill_date, subtotal, tax, total, bill_text) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    self.bill_number,
                    customer_id,
                    bill_date,
                    subtotal,
                    tax,
                    total,
                    bill_text
                )
            )

            bill_id = bill_cursor.lastrowid

            for item in self.cart:
                conn.execute(
                    "INSERT INTO bill_items "
                    "(bill_id, product_id, quantity, price, amount) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (
                        bill_id,
                        item["product_id"],
                        item["quantity"],
                        item["price"],
                        item["amount"]
                    )
                )

                # Stock cannot become negative because of the WHERE condition.
                updated = conn.execute(
                    "UPDATE products "
                    "SET stock = stock - ? "
                    "WHERE product_id = ? AND stock >= ?",
                    (
                        item["quantity"],
                        item["product_id"],
                        item["quantity"]
                    )
                ).rowcount

                if updated != 1:
                    raise ValueError(
                        f"Stock changed while billing '{item['product']}'. "
                        "Please try again."
                    )

            conn.commit()
            self.bill_saved_to_db = True
            return True

        except sqlite3.IntegrityError as e:
            conn.rollback()
            messagebox.showerror(
                "Database Integrity Error",
                f"Bill was not saved.\n\n{e}"
            )
            return False

        except Exception as e:
            conn.rollback()
            messagebox.showerror(
                "Database Error",
                f"Bill was not saved.\n\n{e}"
            )
            return False

    # ==============================================================
    # CREATE BILL TEXT
    # ==============================================================

    def create_bill_text(self):

        customer_name = self.entry_name.get().strip()
        mobile = self.entry_mob.get().strip()
        email = self.entry_email.get().strip()

        subtotal = sum(item["amount"] for item in self.cart)
        tax = subtotal * self.tax_rate / 100
        total = subtotal + tax

        width = 48

        lines = []
        lines.append("=" * width)
        lines.append("              JAISWAL SUPERMARKET")
        lines.append("=" * width)
        lines.append(f"Bill Number : {self.bill_number}")
        lines.append(
            f"Date        : {datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')}"
        )
        lines.append("-" * width)
        lines.append("CUSTOMER DETAILS")
        lines.append("-" * width)
        lines.append(f"Name        : {customer_name}")
        lines.append(f"Mobile No.  : {mobile}")
        lines.append(f"Email       : {email}")
        lines.append("-" * width)

        lines.append(
            f"{'Product':<20}{'Price':>8}{'Qty':>6}{'Amount':>12}"
        )
        lines.append("-" * width)

        for item in self.cart:
            product = item["product"]
            if len(product) > 20:
                product = product[:20]

            lines.append(
                f"{product:<20}"
                f"{item['price']:>8.2f}"
                f"{item['quantity']:>6}"
                f"{item['amount']:>12.2f}"
            )

        lines.append("-" * width)
        lines.append(f"{'Subtotal':<34}{subtotal:>14.2f}")
        lines.append(
            f"{f'Gov Tax ({self.tax_rate:g}%)':<34}{tax:>14.2f}"
        )
        lines.append(f"{'TOTAL':<34}{total:>14.2f}")
        lines.append("=" * width)
        lines.append("             THANK YOU FOR SHOPPING")
        lines.append("=" * width)

        return "\n".join(lines)

    # ==============================================================
    # SAVE BILL AS TXT
    # ==============================================================

    def save_bill(self):

        if not self.cart:
            messagebox.showerror(
                "Empty Bill",
                "Please add products and generate the bill first."
            )
            return

        if not self.validate_customer():
            return

        if not self.save_bill_to_database():
            return

        bill = self.create_bill_text()

        self.textarea.delete("1.0", END)
        self.textarea.insert(END, bill)

        default_name = f"Bill_{self.bill_number}.txt"

        file_path = filedialog.asksaveasfilename(
            title="Save Bill",
            initialdir=self.bill_folder,
            initialfile=default_name,
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")]
        )

        if not file_path:
            return

        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(bill)

            messagebox.showinfo(
                "Bill Saved",
                f"Bill saved successfully.\n\n{file_path}"
            )

        except Exception as e:
            messagebox.showerror(
                "Save Error",
                f"Could not save bill.\n\n{e}"
            )

    # ==============================================================
    # PRINT BILL
    # ==============================================================
    #
    # On Windows, this sends the saved TXT file to the default printer.
    # If printing is unavailable, the user can still save the TXT file.
    # ==============================================================

    def print_bill(self):

        if not self.cart:
            messagebox.showerror(
                "Empty Bill",
                "Please add products and generate the bill first."
            )
            return

        if not self.validate_customer():
            return

        bill = self.create_bill_text()

        self.textarea.delete("1.0", END)
        self.textarea.insert(END, bill)

        # Save temporary printable file
        print_path = os.path.join(
            self.bill_folder,
            f"Print_{self.bill_number}.txt"
        )

        try:
            with open(print_path, "w", encoding="utf-8") as file:
                file.write(bill)

            if sys.platform.startswith("win"):

                try:
                    os.startfile(print_path, "print")

                    messagebox.showinfo(
                        "Print",
                        "The bill has been sent to your default printer."
                    )

                except Exception:
                    messagebox.showwarning(
                        "Print",
                        "Windows could not start printing.\n\n"
                        "The bill has been saved as a TXT file instead:\n"
                        f"{print_path}"
                    )

            else:
                messagebox.showinfo(
                    "Print",
                    "Automatic printing is configured for Windows.\n\n"
                    f"Bill saved here:\n{print_path}"
                )

        except Exception as e:
            messagebox.showerror(
                "Print Error",
                f"Could not prepare the bill for printing.\n\n{e}"
            )

    # ==============================================================
    # SEARCH BILL
    # ==============================================================

    def search_bill(self):

        bill_number = self.entry_search.get().strip()

        if not bill_number:
            messagebox.showerror(
                "Search",
                "Please enter a bill number."
            )
            self.entry_search.focus()
            return

        # Search SQLite first.
        clean_number = bill_number.replace("Bill_", "").replace(".txt", "")

        row = self.db.conn.execute(
            "SELECT bill_text FROM bills WHERE bill_number = ?",
            (clean_number,)
        ).fetchone()

        # Also support entering the full Bill_XXXXXXXXXXXXXX text.
        if not row:
            row = self.db.conn.execute(
                "SELECT bill_text FROM bills WHERE bill_number = ?",
                (bill_number.replace("Bill_", "").replace(".txt", ""),)
            ).fetchone()

        if row:
            self.textarea.delete("1.0", END)
            self.textarea.insert(END, row[0])
            messagebox.showinfo("Bill Found", "Bill loaded from database.")
            return

        # Backward-compatible fallback for older TXT bills.
        file_name = (
            bill_number if bill_number.startswith("Bill_")
            else f"Bill_{bill_number}"
        )
        if not file_name.lower().endswith(".txt"):
            file_name += ".txt"

        file_path = os.path.join(self.bill_folder, file_name)

        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    bill = file.read()

                self.textarea.delete("1.0", END)
                self.textarea.insert(END, bill)
                messagebox.showinfo("Bill Found", "Bill loaded from TXT file.")
                return

            except Exception as e:
                messagebox.showerror(
                    "Search Error",
                    f"Could not read the bill.\n\n{e}"
                )
                return

        messagebox.showerror(
            "Bill Not Found",
            f"No bill found for: {bill_number}"
        )

    # ==============================================================
    # CUSTOMER VALIDATION
    # ==============================================================

    def validate_customer(self):

        name = self.entry_name.get().strip()
        mobile = self.entry_mob.get().strip()
        email = self.entry_email.get().strip()

        if not name:
            messagebox.showerror(
                "Customer Details",
                "Please enter customer name."
            )
            self.entry_name.focus()
            return False

        if not mobile:
            messagebox.showerror(
                "Customer Details",
                "Please enter mobile number."
            )
            self.entry_mob.focus()
            return False

        # Basic mobile validation
        if not mobile.isdigit() or len(mobile) != 10:
            messagebox.showerror(
                "Customer Details",
                "Please enter a valid 10-digit mobile number."
            )
            self.entry_mob.focus()
            return False

        if not email:
            messagebox.showerror(
                "Customer Details",
                "Please enter customer email."
            )
            self.entry_email.focus()
            return False

        if "@" not in email or "." not in email:
            messagebox.showerror(
                "Customer Details",
                "Please enter a valid email address."
            )
            self.entry_email.focus()
            return False

        return True

    # ==============================================================
    # CLEAR
    # ==============================================================

    def clear_all(self):

        answer = messagebox.askyesno(
            "Clear",
            "Do you want to clear the current bill?"
        )

        if not answer:
            return

        self.cart.clear()

        # Customer fields
        self.entry_mob.delete(0, END)
        self.entry_name.delete(0, END)
        self.entry_email.delete(0, END)

        # Product fields
        self.combo_category.current(0)
        self.combo_Subcategory.set("")
        self.combo_ProductName.set("")
        self.combo_price.set("")
        self.combo_Subcategory["values"] = ()
        self.combo_ProductName["values"] = ()
        self.combo_price["values"] = ()

        self.entry_qty.delete(0, END)

        # Totals
        self.set_entry(self.entry_subtotal, "")
        self.set_entry(self.entry_tax, "")
        self.set_entry(self.entry_amoutTotal, "")

        # Bill area
        self.textarea.delete("1.0", END)

        # New bill number
        self.bill_number = self.create_bill_number()
        self.bill_saved_to_db = False

    # ==============================================================
    # EXIT
    # ==============================================================

    def exit_app(self):

        answer = messagebox.askyesno(
            "Exit",
            "Do you really want to exit?"
        )

        if answer:
            try:
                self.db.close()
            finally:
                self.root.destroy()

    # ==============================================================
    # HELPER
    # ==============================================================

    def set_entry(self, entry, value):

        entry.delete(0, END)
        entry.insert(0, value)


# ==============================================================
# MAIN
# ==============================================================

if __name__ == '__main__':

    root = Tk()
    app = Billing_App(root)
    root.mainloop()
