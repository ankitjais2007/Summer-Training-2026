from tkinter import *
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from datetime import datetime
import os
import sys


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

        if category in self.products:

            subcategories = list(self.products[category].keys())
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

        if category in self.products and subcategory in self.products[category]:

            products = list(self.products[category][subcategory].keys())
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

        if (
            category in self.products
            and subcategory in self.products[category]
            and product in self.products[category][subcategory]
        ):
            price = self.products[category][subcategory][product]

            self.combo_price["values"] = [price]
            self.combo_price.current(0)

    # ==============================================================
    # ADD TO CART
    # ==============================================================

    def add_to_cart(self):

        category = self.combo_category.get()
        subcategory = self.combo_Subcategory.get()
        product = self.combo_ProductName.get()
        price_text = self.combo_price.get()
        qty_text = self.entry_qty.get().strip()

        # Validation
        if category == "Select Option" or not category:
            messagebox.showerror("Error", "Please select a category.")
            return

        if not subcategory:
            messagebox.showerror("Error", "Please select a subcategory.")
            return

        if not product:
            messagebox.showerror("Error", "Please select a product.")
            return

        if not price_text:
            messagebox.showerror("Error", "Product price is not available.")
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

        price = float(price_text)
        amount = price * quantity

        # Add item to cart
        self.cart.append({
            "category": category,
            "subcategory": subcategory,
            "product": product,
            "price": price,
            "quantity": quantity,
            "amount": amount
        })

        messagebox.showinfo(
            "Added",
            f"{product} added to cart.\nQuantity: {quantity}\nAmount: ₹{amount:.2f}"
        )

        # Clear only product selection area for next item
        self.entry_qty.delete(0, END)

        # Update subtotal immediately
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

        self.update_totals()

        bill = self.create_bill_text()

        self.textarea.delete("1.0", END)
        self.textarea.insert(END, bill)

        messagebox.showinfo(
            "Bill Generated",
            f"Bill #{self.bill_number} generated successfully."
        )

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

        # Make sure bill is visible/generated
        bill = self.create_bill_text()
        self.textarea.delete("1.0", END)
        self.textarea.insert(END, bill)

        default_name = f"Bill_{self.bill_number}.txt"
        default_path = os.path.join(self.bill_folder, default_name)

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

        # Allow user to enter either:
        # 20260910123456
        # or Bill_20260910123456
        if bill_number.startswith("Bill_"):
            file_name = bill_number
        else:
            file_name = f"Bill_{bill_number}.txt"

        if not file_name.lower().endswith(".txt"):
            file_name += ".txt"

        file_path = os.path.join(self.bill_folder, file_name)

        if not os.path.exists(file_path):

            # Also search all txt files in bills folder
            found_path = None

            for name in os.listdir(self.bill_folder):
                if (
                    name.lower().endswith(".txt")
                    and bill_number.lower() in name.lower()
                ):
                    found_path = os.path.join(self.bill_folder, name)
                    break

            if found_path:
                file_path = found_path
            else:
                messagebox.showerror(
                    "Bill Not Found",
                    f"No bill found for: {bill_number}"
                )
                return

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                bill = file.read()

            self.textarea.delete("1.0", END)
            self.textarea.insert(END, bill)

            messagebox.showinfo(
                "Bill Found",
                "Bill loaded successfully."
            )

        except Exception as e:
            messagebox.showerror(
                "Search Error",
                f"Could not read the bill.\n\n{e}"
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

    # ==============================================================
    # EXIT
    # ==============================================================

    def exit_app(self):

        answer = messagebox.askyesno(
            "Exit",
            "Do you really want to exit?"
        )

        if answer:
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
