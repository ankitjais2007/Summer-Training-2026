from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk 

class Billing_App:
    def __init__(self,root):

        self.root=root
        self.root.geometry("1530x800+0+0")
        self.root.title(" SUPERMARKET BILLING SOFTWARE")

        # Product Categories list
        self.Category=["Select Option","Clothing","LifeStyle","Mobiles"]

        # SubCatClothing
        self.SubCatClothing=["Pant","T-Shirt","Shirt"]
        self.pant=["Levis","Mufti","Spykar"]
        self.price_levis=5000
        self.price_mufti=7000
        self.price_spykar=8000

        self.T_shirt=['Polo','Roadster','Jack&Jones']
        self.price_polo=1500
        self.price_Roadster=1800
        self.price_JackJones=1700

        self.Shirt=['Peter England','Louis Phillipe','Park Avenue']
        self.price_Peter=2100
        self.price_Louis=2700
        self.price_Park=1740

        # SubCatLifStyle
        self.SubCatLifStyle=['Bath Soap','Face Creame','Hair Oil']
        self.Bath_soap=['LifeBuy','Lux','Santoor','Pearl']
        self.price_life=float(20)
        self.price_lux=20
        self.price_santoor=20
        self.price_pearl=30

        self.Face_creame=['Fair&Lovely','Ponds','Olay','Garnier']
        self.price_fair=20
        self.price_ponds=20
        self.price_olay=20
        self.price_garnier=30

        self.Hair_oil=['Parachute','Jashmin','Bajaj']
        self.price_para=25
        self.price_jashmin=22
        self.price_bajaj=30

        # SubCatMobiles
        self.SubCatMobiles=['Iphone','Sumsung','Xiome','RealMe','One+']
        self.Iphone=['Iphone_X','Iphone_11','Iphone_12']
        self.price_ix=40000
        self.price_i11=60000
        self.price_i12=85000

        self.Samsung=['Samsung M16','Sumsung M12','Samsung M21']
        self.price_sm16=16000
        self.price_sm12=12000
        self.price_sm21=18000

        self.Xiome=['Red11','Redme-12','RedmePro']
        self.price_r11=11000
        self.price_r12=12000
        self.price_rpro=9000

        self.RealMe=['RealMe 12','RealMe 13','RealMe Pro']
        self.price_rel12=25000
        self.price_rel13=22000
        self.price_relpro=30000

        self.OnePlus=['OnePlus1','OnePlus2','OnePlus3']
        self.price_one1=45000
        self.price_one12=60000
        self.price_one3=45800



        #Image1
        img1=Image.open("images/img1.jpg")
        img1=img1.resize((500,130),Image.Resampling.LANCZOS)
        self.photoimg1=ImageTk.PhotoImage(img1)

        lbl_img1=Label(self.root,image=self.photoimg1)
        lbl_img1.place(x=0,y=0,width=500,height=130)

        #Image2
        img2=Image.open("images/img2.jpg")
        img2=img2.resize((500,130),Image.Resampling.LANCZOS)
        self.photoimg2=ImageTk.PhotoImage(img2)

        lbl_img2=Label(self.root,image=self.photoimg2)
        lbl_img2.place(x=500,y=0,width=500,height=130)

        #Image3
        img3=Image.open("images/img3.jpg")
        img3=img3.resize((500,130),Image.Resampling.LANCZOS)
        self.photoimg3=ImageTk.PhotoImage(img3)

        lbl_img3=Label(self.root,image=self.photoimg3)
        lbl_img3.place(x=1000,y=0,width=500,height=130)

        # welcome to jaiswal supermarket - label
        lbl_title=Label(self.root,text="WELCOME TO JAISWAL SUPERMARKET", font=('times new roman', 30, "bold"),bg='white',fg='navy')
        lbl_title.place(x=0,y=130, width=1530,height=42)

        # Frame or field after Supermarket Label
        Main_Frame=Frame(self.root,bd=5,relief=GROOVE, bg='white')
        Main_Frame.place(x=0,y=175, width=1530,height=605)

        #Customer LabelFrame
        Cust_Frame=LabelFrame(Main_Frame,text='Customer',font=('times new roman', 12, "bold"),bg='white',fg='red')
        Cust_Frame.place(x=10,y=5,width=350,height=140)

        #mobile number
        lbl_mob=Label(Cust_Frame,text="Mobile No.",font=('times new roman', 12, "bold"),bg='white')
        lbl_mob.grid(row=0,column=0,stick=W,padx=5,pady=2)

        entry_mob=ttk.Entry(Cust_Frame,font=('times new roman', 10, "bold"),width=25)
        entry_mob.grid(row=0,column=1,stick=W,padx=5,pady=2)

        #customername
        lbl_name=Label(Cust_Frame,text="Customer Name",font=('times new roman', 12, "bold"),bg='white')
        lbl_name.grid(row=1,column=0,stick=W,padx=5,pady=2)

        entry_name=ttk.Entry(Cust_Frame,font=('times new roman', 10, "bold"),width=25)
        entry_name.grid(row=1,column=1,stick=W,padx=5,pady=2)

        lbl_email=Label(Cust_Frame,text="Email",font=('times new roman', 12, "bold"),bg='white')
        lbl_email.grid(row=2,column=0,stick=W,padx=5,pady=2)

        entry_email=ttk.Entry(Cust_Frame,font=('times new roman', 10, "bold"),width=25)
        entry_email.grid(row=2,column=1,stick=W,padx=5,pady=2)


        #product LabelFrame
        Product_Frame=LabelFrame(Main_Frame,text='Product',font=('times new roman', 12, "bold"),bg='white',fg='red')
        Product_Frame.place(x=375,y=5,width=570,height=140)

        #select category
        lbl_category=Label(Product_Frame,text="Select Category",font=('times new roman', 12, "bold"),bg='white')
        lbl_category.grid(row=0,column=0,stick=W,padx=5,pady=2)

        combo_category=ttk.Combobox(Product_Frame,value=self.Category,font=('times new roman', 10, "bold"),width=25,state='readonly')
        combo_category.current(0)
        combo_category.grid(row=0,column=1,stick=W,padx=5,pady=2)

        #subcategory
        lbl_Subcategory=Label(Product_Frame,text="Subcategory",font=('times new roman', 12, "bold"),bg='white')
        lbl_Subcategory.grid(row=1,column=0,stick=W,padx=5,pady=2)

        combo_Subcategory=ttk.Combobox(Product_Frame,font=('times new roman', 10, "bold"),width=25,state='readonly')
        combo_Subcategory.grid(row=1,column=1,stick=W,padx=5,pady=2)

        #Product Name
        lbl_ProductName=Label(Product_Frame,text="Product Name",font=('times new roman', 12, "bold"),bg='white')
        lbl_ProductName.grid(row=2,column=0,stick=W,padx=5,pady=2)

        combo_ProductName=ttk.Combobox(Product_Frame,font=('times new roman', 10, "bold"),width=25,state='readonly')
        combo_ProductName.grid(row=2,column=1,stick=W,padx=5,pady=2)

        #Price
        lbl_price=Label(Product_Frame,text="Price",font=('times new roman', 12, "bold"),bg='white')
        lbl_price.grid(row=0,column=2,stick=W,padx=5,pady=2)

        combo_price=ttk.Combobox(Product_Frame,font=('times new roman', 10, "bold"),width=20,state='readonly')
        combo_price.grid(row=0,column=3,stick=W,padx=5,pady=2)

        #Quantity
        qty=Label(Product_Frame,text='Qty',font=("times new roman",10,"bold"),bg='white')
        qty.grid(row=1,column=2,stick=W,padx=5,pady=2)

        entry_qty=ttk.Entry(Product_Frame,font=('times new roman', 10, "bold"),width=23)
        entry_qty.grid(row=1,column=3,stick=W,padx=5,pady=2)





        # right_Frame- Bill area
        bill_number=ttk.Label(Main_Frame,text="Bill Number")
        bill_number.place(x=970,y=12)

        entry_search=ttk.Entry(Main_Frame,font=('times new roman', 10, "bold"),width=25)
        entry_search.place(x=1050,y=12)

        btn_search=Button(Main_Frame,width=10,text='Search',font=('arial', 10, "bold"),bg='green',fg='white',cursor='hand2')
        btn_search.place(x=1250,y=10)

        #Bill area
        RightLabelFrame=LabelFrame(Main_Frame,text='Bill Area',font=('times new roman', 12, "bold"),bg='white',fg='red')

        RightLabelFrame.place(x=1000,y=50,width=500,height=530)

        scroll_y=Scrollbar(RightLabelFrame,orient=VERTICAL)
        textarea=Text(RightLabelFrame,yscrollcommand=scroll_y.set,bg='white',fg='blue',font=('times new roman', 12, "bold"))
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_y.config(command=textarea.yview)
        textarea.pack(fill=BOTH,expand=1)


        #Bill Counter labelFrame
        BillCounterFrame=LabelFrame(Main_Frame,text='Bill Area',font=('times new roman', 12, "bold"),bg='white',fg='red')

        BillCounterFrame.place(x=10,y=160,width=940,height=420)

        #Subtotal
        lbl_subtotal=Label(BillCounterFrame,text="Subtotal",font=('times new roman', 12, "bold"),bg='white')
        lbl_subtotal.grid(row=0,column=0,stick=W,padx=10,pady=20)

        entry_subtotal=ttk.Entry(BillCounterFrame,font=('times new roman', 10, "bold"),width=25)
        entry_subtotal.grid(row=0,column=1,stick=W,padx=10,pady=20)

        #tax
        lbl_tax=Label(BillCounterFrame,text="Gov Tax",font=('times new roman', 12, "bold"),bg='white')
        lbl_tax.grid(row=1,column=0,stick=W,padx=10,pady=20)

        entry_tax=ttk.Entry(BillCounterFrame,font=('times new roman', 10, "bold"),width=25)
        entry_tax.grid(row=1,column=1,stick=W,padx=10,pady=20)

        #amoutTotal
        lbl_amoutTotal=Label(BillCounterFrame,text="Total",font=('times new roman', 12, "bold"),bg='white')
        lbl_amoutTotal.grid(row=2,column=0,stick=W,padx=10,pady=20)

        entry_amoutTotal=ttk.Entry(BillCounterFrame,
        font=('times new roman', 10, "bold"),width=25)
        entry_amoutTotal.grid(row=2,column=1,stick=W,padx=10,pady=20)

        #button Frame
        ButtonFrame=Frame(BillCounterFrame,bd=2,bg='white')
        ButtonFrame.place(x=350,y=20)

        addCart=Button(ButtonFrame,text='Add To Cart',font=('arial', 15, "bold"),bg='orangered',fg='white',cursor='hand2')
        addCart.grid(row=0,column=0,padx=10,pady=10)

        generateBill=Button(ButtonFrame,text='Generate Bill',font=('arial', 15, "bold"),bg='orangered',fg='white',cursor='hand2')
        generateBill.grid(row=0,column=1,padx=10,pady=10)

        save=Button(ButtonFrame,width=10,text='Save Bill',font=('arial', 15, "bold"),bg='orangered',fg='white',cursor='hand2')
        save.grid(row=0,column=2,padx=10,pady=10)

        printBill=Button(ButtonFrame,width=10,text='Print',font=('arial', 15, "bold"),bg='orangered',fg='white',cursor='hand2')
        printBill.grid(row=1,column=0,padx=10,pady=10)

        clear=Button(ButtonFrame,width=11,text='Clear',font=('arial', 15, "bold"),bg='orangered',fg='white',cursor='hand2')
        clear.grid(row=1,column=1,padx=10,pady=10)

        btn_exit=Button(ButtonFrame,width=10,text='Exit',font=('arial', 15, "bold"),bg='orangered',fg='white',cursor='hand2')
        btn_exit.grid(row=1,column=2,padx=10,pady=10)





        



        


        









if __name__=='__main__':
    root=Tk()
    app=Billing_App(root)
    root.mainloop()



