from datetime import datetime

class BillingService:
    TAX_PERCENT=5.0
    def __init__(self,db): 
        self.db=db
    def validate_product(self,name,category,price,stock):
        name=name.strip();
        category=category.strip()
        if not name: 
            raise ValueError('Product name is required.')
        try:
             price=float(price); 
             stock=int(stock)
        except ValueError: 
            raise ValueError('Price must be a number and stock an integer.')
        if price<0 or stock<0:
            raise ValueError('Price and stock cannot be negative.')
        return name,category,price,stock
    def line_total(self,price,qty):
        return round(price*qty,2)
    def totals(self,cart,discount):
        discount=max(0,float(discount));
        subtotal=round(sum(x['total'] for x in cart),2)
        discount_amt=round(subtotal*discount/100,2); taxable=subtotal-discount_amt
        tax=round(taxable*self.TAX_PERCENT/100,2); 
        total=round(taxable+tax,2)
        return subtotal,discount_amt,tax,total
    def invoice_number(self): 
        return 'INV-'+datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]
    def save_bill(self,name,phone,payment,cart,discount):
        if not cart: 
            raise ValueError('Cart is empty.')
        subtotal,disc,tax,total=self.totals(cart,discount)
        return self.db.create_invoice(self.invoice_number(),name.strip(),phone.strip(),datetime.now().strftime('%Y-%m-%d %H:%M:%S'),subtotal,disc,tax,total,payment,cart)
    def invoice_data(self,iid):
        inv,items=self.db.get_invoice(iid)
        if inv is None:return None
        return {'invoice_no':inv['invoice_no'],'customer':inv['customer_name'],'phone':inv['customer_phone'],'date':inv['invoice_date'],'payment':inv['payment_mode'],'subtotal':inv['subtotal'],'discount':inv['discount'],'tax':inv['tax'],'total':inv['grand_total'],
                'items':[{'name':x['product_name'],'price':x['unit_price'],'qty':x['quantity'],'total':x['line_total']} for x in items]}
import tkinter as tk
from tkinter import ttk,messagebox

import tkinter as tk
from tkinter import ttk, messagebox
from invoice import show_invoice


class BillingFrame(ttk.Frame):
    def __init__(self,parent,service,on_data_changed=None):
        super().__init__(parent,padding=15);
        self.service=service; self.changed=on_data_changed; self.cart=[]
        self.customer=tk.StringVar(); 
        self.phone=tk.StringVar(); 
        self.payment=tk.StringVar(value='Cash'); 
        self.discount=tk.StringVar(value='0');
        self.build(); self.refresh_products()
    def build(self):
        ttk.Label(self,text='Create New Bill',style='Heading.TLabel').pack(anchor='w',pady=(0,8))
        c=ttk.LabelFrame(self,text='Customer Details',padding=8); 
        c.pack(fill='x')
        for col,label,var in [(0,'Customer',self.customer),(2,'Phone',self.phone)]: ttk.Label(c,text=label).grid(row=0,column=col,padx=5); ttk.Entry(c,textvariable=var,width=22).grid(row=0,column=col+1,padx=5)
        ttk.Label(c,text='Payment').grid(row=0,column=4,padx=5);
        ttk.Combobox(c,textvariable=self.payment,values=['Cash','UPI','Card'],state='readonly',width=10).grid(row=0,column=5,padx=5)
        main=ttk.Frame(self)
        main.pack(fill='both',expand=True,pady=10)
        l=ttk.LabelFrame(main,text='Products',padding=6);
        l.pack(side='left',fill='both',expand=True,padx=(0,5))
        self.pt=ttk.Treeview(l,columns=('id','name','price','stock'),show='headings',height=10)
        for c,h,w in [('id','ID',50),('name','Name',180),('price','Price',90),('stock','Stock',70)]:self.pt.heading(c,text=h);
        self.pt.column(c,width=w)
        self.pt.pack(fill='both',expand=True); 
        a=ttk.Frame(l);a.pack(fill='x',pady=6);
        ttk.Label(a,text='Qty').pack(side='left');
        self.qty=tk.StringVar(value='1');
        ttk.Spinbox(a,from_=1,to=999,textvariable=self.qty,width=6).pack(side='left',padx=5);
        ttk.Button(a,text='Add to Cart',style='Accent.TButton',command=self.add).pack(side='left')
        r=ttk.LabelFrame(main,text='Cart',padding=6);
        r.pack(side='right',fill='both',expand=True,padx=(5,0))
        self.ct=ttk.Treeview(r,columns=('name','price','qty','total'),show='headings',height=10)
        for c,h,w in [('name','Name',160),('price','Price',80),('qty','Qty',60),('total','Total',90)]:self.ct.heading(c,text=h);
        self.ct.column(c,width=w)
        self.ct.pack(fill='both',expand=True);ttk.Button(r,text='Remove Selected',command=self.remove).pack(anchor='w',pady=6)
        summary=ttk.Frame(self);summary.pack(fill='x'); ttk.Label(summary,text='Discount %').pack(side='left');
        ttk.Entry(summary,textvariable=self.discount,width=8).pack(side='left',padx=5); 
        ttk.Button(summary,text='Recalculate',command=self.recalc).pack(side='left',padx=5);
        self.sub=tk.StringVar();
        self.disc=tk.StringVar();
        self.tax=tk.StringVar();
        self.total=tk.StringVar();
        for label,var in [('Subtotal',self.sub),('Discount',self.disc),('GST 5%',self.tax),('Grand Total',self.total)]:ttk.Label(summary,text=label).pack(side='left',padx=(15,2));ttk.Label(summary,textvariable=var,style='Heading.TLabel').pack(side='left',padx=3)
        ttk.Button(summary,text='Clear',command=self.clear).pack(side='right',padx=4);ttk.Button(summary,text='Generate Bill',style='Accent.TButton',command=self.generate).pack(side='right',padx=4);
        self.recalc()
    def refresh_products(self):
        if not hasattr(self,'pt'):return
        for x in self.pt.get_children():self.pt.delete(x)
        for p in self.service.db.get_products():self.pt.insert('','end',iid=str(p['id']),values=(p['id'],p['name'],f"₹{p['price']:.2f}",p['stock']))
    def add(self):
        s=self.pt.selection()
        if not s:return messagebox.showwarning('Select','Select a product.')
        try:q=int(self.qty.get());assert q>0
        except: return messagebox.showerror('Quantity','Enter a positive integer.')
        p=self.service.db.get_product(int(s[0])); old=next((x['qty'] for x in self.cart if x['product_id']==p['id']),0)
        if old+q>p['stock']:return messagebox.showwarning('Stock',f"Only {p['stock']} available.")
        for x in self.cart:
            if x['product_id']==p['id']:x['qty']+=q;x['total']=self.service.line_total(x['price'],x['qty']);break
        else:self.cart.append({'product_id':p['id'],'name':p['name'],'price':p['price'],'qty':q,'total':self.service.line_total(p['price'],q)})
        self.refresh_cart()
    def refresh_cart(self):
        for x in self.ct.get_children():self.ct.delete(x)
        for i,x in enumerate(self.cart):self.ct.insert('','end',iid=str(i),values=(x['name'],f"₹{x['price']:.2f}",x['qty'],f"₹{x['total']:.2f}"))
        self.recalc()
    def remove(self):
        s=self.ct.selection()
        if s:self.cart.pop(int(s[0]));self.refresh_cart()
    def recalc(self):
        try:d=float(self.discount.get() or 0)
        except:d=0
        a,b,c,e=self.service.totals(self.cart,d);self.sub.set(f'₹{a:.2f}');self.disc.set(f'₹{b:.2f}');self.tax.set(f'₹{c:.2f}');self.total.set(f'₹{e:.2f}')
    def generate(self):
        try:
            d=float(self.discount.get() or 0)
            if not 0<=d<=100:raise ValueError('Discount must be between 0 and 100.')
            iid=self.service.save_bill(self.customer.get(),self.phone.get(),self.payment.get(),self.cart,d);self.show(self.service.invoice_data(iid));self.clear();self.changed and self.changed()
        except Exception as e:messagebox.showerror('Could Not Generate Bill',str(e))
    def show(self,inv):
        w=tk.Toplevel(self);w.title(inv['invoice_no']);w.geometry('500x560');t=tk.Text(w,font=('Consolas',10));t.pack(fill='both',expand=True,padx=10,pady=10)
        lines=['           SIMPLE BILLING SYSTEM','='*48,f"Invoice : {inv['invoice_no']}",f"Date    : {inv['date']}",f"Customer: {inv['customer'] or 'Walk-in'}",f"Phone   : {inv['phone'] or '-'}",f"Payment : {inv['payment']}",'-'*48,f"{'Item':<22}{'Qty':>5}{'Total':>15}",'-'*48]
        lines += [f"{x['name'][:22]:<22}{x['qty']:>5}{x['total']:>15.2f}" for x in inv['items']]
        lines += ['-'*48,f"{'Subtotal':<32}{inv['subtotal']:>15.2f}",f"{'Discount':<32}{inv['discount']:>15.2f}",f"{'GST (5%)':<32}{inv['tax']:>15.2f}",'='*48,f"{'GRAND TOTAL':<32}{inv['total']:>15.2f}",'='*48]
        t.insert('1.0','\n'.join(lines));
        t.config(state='disabled');
        ttk.Button(w,text='Close',command=w.destroy).pack(pady=6)
    def clear(self):
        self.customer.set('');
        self.phone.set('');
        self.payment.set('Cash');
        self.discount.set('0');
        self.cart.clear();self.refresh_cart()
