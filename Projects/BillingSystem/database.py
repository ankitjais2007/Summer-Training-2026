import sqlite3
from pathlib import Path

DB_PATH = "billing.db"

class Database:
    def __init__(self, path=DB_PATH):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute('PRAGMA foreign_keys = ON')
        self.create_tables()
        # self.seed_products()

    def create_tables(self):
        self.conn.executescript('''
        CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            category TEXT DEFAULT '',
            price REAL NOT NULL CHECK(price >= 0),
            stock INTEGER NOT NULL CHECK(stock >= 0));
        CREATE TABLE IF NOT EXISTS invoices(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_no TEXT NOT NULL UNIQUE,
            customer_name TEXT DEFAULT '', customer_phone TEXT DEFAULT '',
            invoice_date TEXT NOT NULL, subtotal REAL NOT NULL,
            discount REAL NOT NULL, tax REAL NOT NULL,
            grand_total REAL NOT NULL, payment_mode TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS invoice_items(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_id INTEGER NOT NULL,
            product_name TEXT NOT NULL, unit_price REAL NOT NULL,
            quantity INTEGER NOT NULL, line_total REAL NOT NULL,
            FOREIGN KEY(invoice_id) REFERENCES invoices(id) ON DELETE CASCADE);
        ''')
        self.conn.commit()

    # def seed_products(self):
    #     if self.conn.execute('SELECT COUNT(*) c FROM products').fetchone()['c'] == 0:
    #         self.conn.executemany(
    #             'INSERT INTO products(name,category,price,stock) VALUES(?,?,?,?)',
    #             [('Wireless Mouse','Computer',500,20),('Keyboard','Computer',800,12),
    #              ('USB Cable','Accessories',200,30),('Pendrive 32GB','Storage',450,15),
    #              ('Laptop Stand','Accessories',900,8)])
    #         self.conn.commit()

    def add_product(self,name,category,price,stock):
        self.conn.execute('INSERT INTO products(name,category,price,stock) VALUES(?,?,?,?)',(name,category,price,stock)); self.conn.commit()
    def get_products(self,search=''):
        if search:
            like=f'%{search}%'
            return self.conn.execute('SELECT * FROM products WHERE name LIKE ? OR category LIKE ? ORDER BY name',(like,like)).fetchall()
        return self.conn.execute('SELECT * FROM products ORDER BY name').fetchall()
    def get_product(self,pid):
        return self.conn.execute('SELECT * FROM products WHERE id=?',(pid,)).fetchone()
    def update_product(self,pid,name,category,price,stock):
        self.conn.execute('UPDATE products SET name=?,category=?,price=?,stock=? WHERE id=?',(name,category,price,stock,pid)); self.conn.commit()
    def delete_product(self,pid):
        self.conn.execute('DELETE FROM products WHERE id=?',(pid,)); self.conn.commit()

    def create_invoice(self, invoice_no, customer_name, phone, date, subtotal, discount, tax, total, payment, items):
        with self.conn:
            cur=self.conn.execute('''INSERT INTO invoices(invoice_no,customer_name,customer_phone,invoice_date,subtotal,discount,tax,grand_total,payment_mode) VALUES(?,?,?,?,?,?,?,?,?)''',
                (invoice_no,customer_name,phone,date,subtotal,discount,tax,total,payment))
            invoice_id=cur.lastrowid
            for item in items:
                product=self.get_product(item['product_id'])
                if product is None: raise ValueError('Product no longer exists.')
                if item['qty'] > product['stock']: raise ValueError(f"Not enough stock for {product['name']}.")
                self.conn.execute('INSERT INTO invoice_items(invoice_id,product_name,unit_price,quantity,line_total) VALUES(?,?,?,?,?)',
                    (invoice_id,item['name'],item['price'],item['qty'],item['total']))
                self.conn.execute('UPDATE products SET stock=stock-? WHERE id=?',(item['qty'],item['product_id']))
            return invoice_id

    def get_invoices(self): return self.conn.execute('SELECT * FROM invoices ORDER BY id DESC').fetchall()
    def get_invoice(self,iid):
        inv=self.conn.execute('SELECT * FROM invoices WHERE id=?',(iid,)).fetchone()
        items=self.conn.execute('SELECT * FROM invoice_items WHERE invoice_id=? ORDER BY id',(iid,)).fetchall()
        return inv,items

    def dashboard(self):
        from datetime import date
        today=date.today().isoformat()
        row=self.conn.execute('SELECT COUNT(*) c, COALESCE(SUM(grand_total),0) sales FROM invoices WHERE invoice_date LIKE ?',(today+'%',)).fetchone()
        products=self.conn.execute('SELECT COUNT(*) c FROM products').fetchone()['c']
        low=self.conn.execute('SELECT * FROM products WHERE stock<=5 ORDER BY stock,name').fetchall()
        return row['sales'],row['c'],products,low
    def close(self): self.conn.close()
