import tkinter as tk
from tkinter import ttk,messagebox

class ProductsFrame(ttk.Frame):
    def __init__(self,parent,service,on_data_changed=None):
        super().__init__(parent,padding=15); 
        self.service=service; 
        self.changed=on_data_changed;
        self.selected_id=None
        self.name=tk.StringVar(); 
        self.category=tk.StringVar(); 
        self.price=tk.StringVar(); 
        self.stock=tk.StringVar();
        self.search=tk.StringVar(); 
        self.build();
        self.refresh_products()
    def build(self):
        ttk.Label(self,text='Product Management',style='Heading.TLabel').pack(anchor='w',pady=(0,10))
        f=ttk.LabelFrame(self,text='Product Details',padding=10);
        f.pack(fill='x')
        for r,(label,var,col) in enumerate([('Name',self.name,0),('Category',self.category,2),('Price',self.price,0),('Stock',self.stock,2)]):
            row=0 if r<2 else 1; ttk.Label(f,text=label).grid(row=row,column=col,padx=5,pady=5,sticky='w'); 
            ttk.Entry(f,textvariable=var,width=22).grid(row=row,column=col+1,padx=5,pady=5)
        b=ttk.Frame(f);
        b.grid(row=2,column=0,columnspan=4,pady=5)
        ttk.Button(b,text='Add Product',style='Accent.TButton',command=self.add).pack(side='left',padx=4); 
        ttk.Button(b,text='Update',command=self.update).pack(side='left',padx=4);
        ttk.Button(b,text='Delete',command=self.delete).pack(side='left',padx=4);
        ttk.Button(b,text='Clear',command=self.clear).pack(side='left',padx=4)
        s=ttk.Frame(self); s.pack(fill='x',pady=10); 
        ttk.Label(s,text='Search').pack(side='left'); 
        ttk.Entry(s,textvariable=self.search,width=30).pack(side='left',padx=7);
        ttk.Button(s,text='Search',command=self.refresh_products).pack(side='left'); 
        ttk.Button(s,text='Show All',command=lambda:(self.search.set(''),self.refresh_products())).pack(side='left',padx=4)
        self.tree=ttk.Treeview(self,columns=('id','name','category','price','stock'),show='headings');
        for c,h,w in [('id','ID',60),('name','Name',250),('category','Category',180),('price','Price',120),('stock','Stock',90)]: self.tree.heading(c,text=h);
        self.tree.column(c,width=w)
        self.tree.pack(fill='both',expand=True);
        self.tree.bind('<<TreeviewSelect>>',self.select)
    def refresh_products(self):
        if not hasattr(self,'tree'): return
        for x in self.tree.get_children(): self.tree.delete(x)
        for p in self.service.db.get_products(self.search.get().strip()): self.tree.insert('', 'end',iid=str(p['id']),values=(p['id'],p['name'],p['category'],f"₹{p['price']:.2f}",p['stock']))
    def select(self,_=None):
        s=self.tree.selection()
        if not s: return
        p=self.service.db.get_product(int(s[0])); self.selected_id=p['id']; self.name.set(p['name']); self.category.set(p['category']); self.price.set(p['price']); self.stock.set(p['stock'])
    def values(self):
        return self.service.validate_product(self.name.get(),self.category.get(),self.price.get(),self.stock.get())
    def add(self):
        try:
            self.service.db.add_product(*self.values());
            messagebox.showinfo('Success','Product added.'); 
            self.clear(); self.refresh_products();
            self.changed and self.changed()
        except Exception as e:
            messagebox.showerror('Error',str(e))
    def update(self):
        if self.selected_id is None:
            return messagebox.showwarning('Select','Select a product first.')
        try:
            self.service.db.update_product(self.selected_id,*self.values());
            self.clear(); 
            self.refresh_products();
            self.changed and self.changed()
        except Exception as e:
            messagebox.showerror('Error',str(e))
    def delete(self):
        if self.selected_id is None:
            return messagebox.showwarning('Select','Select a product first.')
        if messagebox.askyesno('Confirm','Delete selected product?'): 
            self.service.db.delete_product(self.selected_id); 
            self.clear(); 
            self.refresh_products();
            self.changed and self.changed();
    def clear(self): 
        self.selected_id=None; 
        self.name.set('');
        self.category.set('');
        self.price.set(''); 
        self.stock.set('');
