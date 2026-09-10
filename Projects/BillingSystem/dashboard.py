from tkinter import ttk

class DashboardFrame(ttk.Frame):
    def __init__(self,parent,service):
        super().__init__(parent,padding=15);
        self.service=service;
        self.sales=__import__('tkinter').StringVar();
        self.bills=__import__('tkinter').StringVar();
        self.products=__import__('tkinter').StringVar();
        self.build();
        self.refresh_dashboard()
    def build(self):
        ttk.Label(self,text='Dashboard',style='Heading.TLabel').pack(anchor='w',pady=(0,15));
        cards=ttk.Frame(self);cards.pack(fill='x')
        for col,(title,var) in enumerate([('Today Sales',self.sales),('Today Bills',self.bills),('Total Products',self.products)]):
            f=ttk.LabelFrame(cards,text=title,padding=20);
            f.grid(row=0,column=col,sticky='nsew',padx=8);
            cards.columnconfigure(col,weight=1);
            ttk.Label(f,textvariable=var,font=('Segoe UI',20,'bold')).pack()
        box=ttk.LabelFrame(self,text='Low Stock (5 or less)',padding=10);
        box.pack(fill='both',expand=True,pady=20);
        self.tree=ttk.Treeview(box,columns=('name','category','stock'),show='headings')
        for c,h,w in [('name','Product',250),('category','Category',180),('stock','Stock',100)]:self.tree.heading(c,text=h);self.tree.column(c,width=w)
        self.tree.pack(fill='both',expand=True)
    def refresh_dashboard(self):
        sales,bills,products,low=self.service.db.dashboard();
        self.sales.set(f'₹{sales:.2f}');
        self.bills.set(str(bills));self.products.set(str(products))
        if hasattr(self,'tree'):
            for x in self.tree.get_children():self.tree.delete(x)
            for p in low:self.tree.insert('','end',values=(p['name'],p['category'],p['stock']))
