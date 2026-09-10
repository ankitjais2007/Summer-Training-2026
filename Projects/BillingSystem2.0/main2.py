from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk


class Billing_App:
    def __init__(self, root):

        self.root = root
        self.root.geometry("1530x800+0+0")
        self.root.title(" SUPERMARKET BILLING SOFTWARE")


        #product
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

        # Category list
        self.Category = [
            "Select Option",
            "Clothing",
            "LifeStyle",
            "Mobiles"
        ]

        # Image 1
        img1 = Image.open("images/img1.jpg")
        img1 = img1.resize((500, 130), Image.Resampling.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)

        lbl_img1 = Label(self.root, image=self.photoimg1)
        lbl_img1.place(x=0, y=0, width=500, height=130)

        # Image 2
        img2 = Image.open("images/img2.jpg")
        img2 = img2.resize((500, 130), Image.Resampling.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)

        lbl_img2 = Label(self.root, image=self.photoimg2)
        lbl_img2.place(x=500, y=0, width=500, height=130)

        # Image 3
        img3 = Image.open("images/img3.jpg")
        img3 = img3.resize((500, 130), Image.Resampling.LANCZOS)
        self.photoimg3 = ImageTk.PhotoImage(img3)

        lbl_img3 = Label(self.root, image=self.photoimg3)
        lbl_img3.place(x=1000, y=0, width=500, height=130)


        lbl_title = Label(
            self.root,
            text="WELCOME TO JAISWAL SUPERMARKET",
            font=('times new roman', 30, "bold"),
            bg='white',
            fg='navy'
        )

        lbl_title.place(x=0, y=130, width=1530, height=42)

        # MAIN FRAME
        Main_Frame = Frame(
            self.root,
            bd=5,
            relief=GROOVE,
            bg='white'
        )

        Main_Frame.place(
            x=0,
            y=175,
            width=1530,
            height=605
        )


        # CUSTOMER FRAME
        Cust_Frame = LabelFrame(
            Main_Frame,
            text='Customer',
            font=('times new roman', 12, "bold"),
            bg='white',
            fg='red'
        )

        Cust_Frame.place(
            x=10,
            y=5,
            width=350,
            height=140
        )

        # Mobile Number
        lbl_mob = Label(
            Cust_Frame,
            text="Mobile No.",
            font=('times new roman', 12, "bold"),
            bg='white'
        )

        lbl_mob.grid(
            row=0,
            column=0,
            sticky=W,
            padx=5,
            pady=2
        )

        entry_mob = ttk.Entry(
            Cust_Frame,
            font=('times new roman', 10, "bold"),
            width=25
        )

        entry_mob.grid(
            row=0,
            column=1,
            sticky=W,
            padx=5,
            pady=2
        )

        # Customer Name
        lbl_name = Label(
            Cust_Frame,
            text="Customer Name",
            font=('times new roman', 12, "bold"),
            bg='white'
        )

        lbl_name.grid(
            row=1,
            column=0,
            sticky=W,
            padx=5,
            pady=2
        )

        entry_name = ttk.Entry(
            Cust_Frame,
            font=('times new roman', 10, "bold"),
            width=25
        )

        entry_name.grid(
            row=1,
            column=1,
            sticky=W,
            padx=5,
            pady=2
        )

        # Email
        lbl_email = Label(
            Cust_Frame,
            text="Email",
            font=('times new roman', 12, "bold"),
            bg='white'
        )

        lbl_email.grid(
            row=2,
            column=0,
            sticky=W,
            padx=5,
            pady=2
        )

        entry_email = ttk.Entry(
            Cust_Frame,
            font=('times new roman', 10, "bold"),
            width=25
        )

        entry_email.grid(
            row=2,
            column=1,
            sticky=W,
            padx=5,
            pady=2
        )


        # PRODUCT FRAME

        Product_Frame = LabelFrame(
            Main_Frame,
            text='Product',
            font=('times new roman', 12, "bold"),
            bg='white',
            fg='red'
        )

        Product_Frame.place(
            x=375,
            y=5,
            width=570,
            height=140
        )

 
        # CATEGORY
        lbl_category = Label(
            Product_Frame,
            text="Select Category",
            font=('times new roman', 12, "bold"),
            bg='white'
        )

        lbl_category.grid(
            row=0,
            column=0,
            sticky=W,
            padx=5,
            pady=2
        )

        self.combo_category = ttk.Combobox(
            Product_Frame,
            values=self.Category,
            font=('times new roman', 10, "bold"),
            width=25,
            state='readonly'
        )

        self.combo_category.current(0)

        self.combo_category.grid(
            row=0,
            column=1,
            sticky=W,
            padx=5,
            pady=2
        )

        # IMPORTANT:
        # When category changes, Categories() will run
        self.combo_category.bind(
            "<<ComboboxSelected>>",
            self.Categories
        )


        # SUBCATEGORY
        lbl_Subcategory = Label(
            Product_Frame,
            text="Subcategory",
            font=('times new roman', 12, "bold"),
            bg='white'
        )

        lbl_Subcategory.grid(
            row=1,
            column=0,
            sticky=W,
            padx=5,
            pady=2
        )

        self.combo_Subcategory = ttk.Combobox(
            Product_Frame,
            font=('times new roman', 10, "bold"),
            width=25,
            state='readonly'
        )

        self.combo_Subcategory.grid(
            row=1,
            column=1,
            sticky=W,
            padx=5,
            pady=2
        )

        # When subcategory changes
        self.combo_Subcategory.bind(
            "<<ComboboxSelected>>",
            self.SubCategories
        )


        # PRODUCT NAME
        
        lbl_ProductName = Label(
            Product_Frame,
            text="Product Name",
            font=('times new roman', 12, "bold"),
            bg='white'
        )

        lbl_ProductName.grid(
            row=2,
            column=0,
            sticky=W,
            padx=5,
            pady=2
        )

        self.combo_ProductName = ttk.Combobox(
            Product_Frame,
            font=('times new roman', 10, "bold"),
            width=25,
            state='readonly'
        )

        self.combo_ProductName.grid(
            row=2,
            column=1,
            sticky=W,
            padx=5,
            pady=2
        )

        # When product changes
        self.combo_ProductName.bind(
            "<<ComboboxSelected>>",
            self.ProductName
        )

       
        # PRICE
        lbl_price = Label(
            Product_Frame,
            text="Price",
            font=('times new roman', 12, "bold"),
            bg='white'
        )

        lbl_price.grid(
            row=0,
            column=2,
            sticky=W,
            padx=5,
            pady=2
        )

        self.combo_price = ttk.Combobox(
            Product_Frame,
            font=('times new roman', 10, "bold"),
            width=20,
            state='readonly'
        )

        self.combo_price.grid(
            row=0,
            column=3,
            sticky=W,
            padx=5,
            pady=2
        )

        # ----------------------------------------------------------
        # QUANTITY
        # ----------------------------------------------------------

        qty = Label(
            Product_Frame,
            text='Qty',
            font=("times new roman", 10, "bold"),
            bg='white'
        )

        qty.grid(
            row=1,
            column=2,
            sticky=W,
            padx=5,
            pady=2
        )

        entry_qty = ttk.Entry(
            Product_Frame,
            font=('times new roman', 10, "bold"),
            width=23
        )

        entry_qty.grid(
            row=1,
            column=3,
            sticky=W,
            padx=5,
            pady=2
        )

        # ==========================================================
        # RIGHT FRAME - BILL SEARCH
        # ==========================================================

        bill_number = ttk.Label(
            Main_Frame,
            text="Bill Number"
        )

        bill_number.place(
            x=970,
            y=12
        )

        entry_search = ttk.Entry(
            Main_Frame,
            font=('times new roman', 10, "bold"),
            width=25
        )

        entry_search.place(
            x=1050,
            y=12
        )

        btn_search = Button(
            Main_Frame,
            width=10,
            text='Search',
            font=('arial', 10, "bold"),
            bg='green',
            fg='white',
            cursor='hand2'
        )

        btn_search.place(
            x=1250,
            y=10
        )

        # BILL AREA
        
        RightLabelFrame = LabelFrame(
            Main_Frame,
            text='Bill Area',
            font=('times new roman', 12, "bold"),
            bg='white',
            fg='red'
        )

        RightLabelFrame.place(
            x=1000,
            y=50,
            width=500,
            height=530
        )

        scroll_y = Scrollbar(
            RightLabelFrame,
            orient=VERTICAL
        )

        textarea = Text(
            RightLabelFrame,
            yscrollcommand=scroll_y.set,
            bg='white',
            fg='blue',
            font=('times new roman', 12, "bold")
        )

        scroll_y.pack(
            side=RIGHT,
            fill=Y
        )

        scroll_y.config(
            command=textarea.yview
        )

        textarea.pack(
            fill=BOTH,
            expand=1
        )

        # BILL COUNTER FRAME
   
        BillCounterFrame = LabelFrame(
            Main_Frame,
            text='Bill Area',
            font=('times new roman', 12, "bold"),
            bg='white',
            fg='red'
        )

        BillCounterFrame.place(
            x=10,
            y=160,
            width=940,
            height=420
        )

        # Subtotal
        lbl_subtotal = Label(
            BillCounterFrame,
            text="Subtotal",
            font=('times new roman', 12, "bold"),
            bg='white'
        )

        lbl_subtotal.grid(
            row=0,
            column=0,
            sticky=W,
            padx=10,
            pady=20
        )

        entry_subtotal = ttk.Entry(
            BillCounterFrame,
            font=('times new roman', 10, "bold"),
            width=25
        )

        entry_subtotal.grid(
            row=0,
            column=1,
            sticky=W,
            padx=10,
            pady=20
        )

        # Tax
        lbl_tax = Label(
            BillCounterFrame,
            text="Gov Tax",
            font=('times new roman', 12, "bold"),
            bg='white'
        )

        lbl_tax.grid(
            row=1,
            column=0,
            sticky=W,
            padx=10,
            pady=20
        )

        entry_tax = ttk.Entry(
            BillCounterFrame,
            font=('times new roman', 10, "bold"),
            width=25
        )

        entry_tax.grid(
            row=1,
            column=1,
            sticky=W,
            padx=10,
            pady=20
        )

        # Total
        lbl_amoutTotal = Label(
            BillCounterFrame,
            text="Total",
            font=('times new roman', 12, "bold"),
            bg='white'
        )

        lbl_amoutTotal.grid(
            row=2,
            column=0,
            sticky=W,
            padx=10,
            pady=20
        )

        entry_amoutTotal = ttk.Entry(
            BillCounterFrame,
            font=('times new roman', 10, "bold"),
            width=25
        )

        entry_amoutTotal.grid(
            row=2,
            column=1,
            sticky=W,
            padx=10,
            pady=20
        )

      
        # BUTTON FRAME
        

        ButtonFrame = Frame(
            BillCounterFrame,
            bd=2,
            bg='white'
        )

        ButtonFrame.place(
            x=350,
            y=20
        )

        addCart = Button(
            ButtonFrame,
            text='Add To Cart',
            font=('arial', 15, "bold"),
            bg='orangered',
            fg='white',
            cursor='hand2'
        )

        addCart.grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        generateBill = Button(
            ButtonFrame,
            text='Generate Bill',
            font=('arial', 15, "bold"),
            bg='orangered',
            fg='white',
            cursor='hand2'
        )

        generateBill.grid(
            row=0,
            column=1,
            padx=10,
            pady=10
        )

        save = Button(
            ButtonFrame,
            width=10,
            text='Save Bill',
            font=('arial', 15, "bold"),
            bg='orangered',
            fg='white',
            cursor='hand2'
        )

        save.grid(
            row=0,
            column=2,
            padx=10,
            pady=10
        )

        printBill = Button(
            ButtonFrame,
            width=10,
            text='Print',
            font=('arial', 15, "bold"),
            bg='orangered',
            fg='white',
            cursor='hand2'
        )

        printBill.grid(
            row=1,
            column=0,
            padx=10,
            pady=10
        )

        clear = Button(
            ButtonFrame,
            width=11,
            text='Clear',
            font=('arial', 15, "bold"),
            bg='orangered',
            fg='white',
            cursor='hand2'
        )

        clear.grid(
            row=1,
            column=1,
            padx=10,
            pady=10
        )

        btn_exit = Button(
            ButtonFrame,
            width=10,
            text='Exit',
            font=('arial', 15, "bold"),
            bg='orangered',
            fg='white',
            cursor='hand2'
        )

        btn_exit.grid(
            row=1,
            column=2,
            padx=10,
            pady=10
        )

    
    # CATEGORY FUNCTION

    def Categories(self, event=""):

        category = self.combo_category.get()

        # Clear previous values
        self.combo_Subcategory.set("")
        self.combo_ProductName.set("")
        self.combo_price.set("")

        self.combo_Subcategory["values"] = ()
        self.combo_ProductName["values"] = ()
        self.combo_price["values"] = ()

        # Check category
        if category in self.products:

            subcategories = list(
                self.products[category].keys()
            )

            self.combo_Subcategory["values"] = subcategories

            # Select first subcategory
            if subcategories:
                self.combo_Subcategory.current(0)

                # Automatically load products
                self.SubCategories()


    # SUBCATEGORY FUNCTION

    def SubCategories(self, event=""):

        category = self.combo_category.get()
        subcategory = self.combo_Subcategory.get()

        # Clear product and price
        self.combo_ProductName.set("")
        self.combo_price.set("")

        self.combo_ProductName["values"] = ()
        self.combo_price["values"] = ()

        if (
            category in self.products
            and subcategory in self.products[category]
        ):

            products = list(
                self.products[category][subcategory].keys()
            )

            self.combo_ProductName["values"] = products

            # Select first product
            if products:
                self.combo_ProductName.current(0)

                # Automatically load price
                self.ProductName()

  
    # PRODUCT NAME FUNCTION
  
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

            # Put price into price ComboBox
            self.combo_price["values"] = [price]
            self.combo_price.current(0)



# MAIN


if __name__ == '__main__':

    root = Tk()

    app = Billing_App(root)

    root.mainloop()