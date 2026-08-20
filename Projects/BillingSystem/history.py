import tkinter as tk
from tkinter import ttk,messagebox

class HistoryFrame(ttk.Frame):
    def __init__(self,parent,service):
        super().__init__(parent,padding=15);self.service=service;self.build();self.refresh_history()
    def build(self):
        ttk.Label(self,text='Invoice History',style='Heading.TLabel').pack(anchor='w',pady=(0,10))
        self.tree=ttk.Treeview(self,columns=('id','no','customer','date','payment','total'),show='headings')
        for c,h,w in [('id','ID',50),('no','Invoice No',190),('customer','Customer',160),('date','Date',170),('payment','Payment',90),('total','Total',100)]:self.tree.heading(c,text=h);self.tree.column(c,width=w)
        self.tree.pack(fill='both',expand=True);ttk.Button(self,text='View Selected Invoice',command=self.view).pack(anchor='w',pady=10);self.tree.bind('<Double-1>',lambda e:self.view())
    def refresh_history(self):
        for x in self.tree.get_children():self.tree.delete(x)
        for i in self.service.db.get_invoices():self.tree.insert('','end',iid=str(i['id']),values=(i['id'],i['invoice_no'],i['customer_name'] or 'Walk-in',i['invoice_date'],i['payment_mode'],f"₹{i['grand_total']:.2f}"))
    def view(self):
        s=self.tree.selection()
        if not s:return messagebox.showwarning('Select','Select an invoice.')
        inv=self.service.invoice_data(int(s[0]));w=tk.Toplevel(self);w.title(inv['invoice_no']);w.geometry('500x560');t=tk.Text(w,font=('Consolas',10));t.pack(fill='both',expand=True,padx=10,pady=10)
        lines=['           SIMPLE BILLING SYSTEM','='*48,f"Invoice : {inv['invoice_no']}",f"Date    : {inv['date']}",f"Customer: {inv['customer'] or 'Walk-in'}",f"Payment : {inv['payment']}",'-'*48]
        lines += [f"{x['name'][:22]:<22}{x['qty']:>5}{x['total']:>15.2f}" for x in inv['items']]
        lines += ['-'*48,f"{'Subtotal':<32}{inv['subtotal']:>15.2f}",f"{'Discount':<32}{inv['discount']:>15.2f}",f"{'GST (5%)':<32}{inv['tax']:>15.2f}",'='*48,f"{'GRAND TOTAL':<32}{inv['total']:>15.2f}"]
        t.insert('1.0','\n'.join(lines));t.config(state='disabled');ttk.Button(w,text='Close',command=w.destroy).pack(pady=6)
