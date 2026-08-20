import sqlite3


class Database:
    def __init__(self, path=DB_PATH):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self._create_tables()
        self._seed_if_empty()


CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT DEFAULT '',
    unit TEXT DEFAULT 'pcs',
    price REAL NOT NULL DEFAULT 0,
    stock INTEGER NOT NULL DEFAULT 0
);


def list_products(self, search=""):
    if search:
        like = f"%{search}%"
        return self.conn.execute(
            "SELECT * FROM products WHERE name LIKE ? OR category LIKE ? "
            "ORDER BY name", (like, like)
        ).fetchall()
    return self.conn.execute("SELECT * FROM products ORDER BY name").fetchall()


def create_invoice(self, customer_name, customer_phone, items, discount_percent,
                    tax_percent, payment_mode):
    subtotal = sum(i["total"] for i in items)
    discount_amount = round(subtotal * discount_percent / 100, 2)
    taxable = subtotal - discount_amount
    tax_amount = round(taxable * tax_percent / 100, 2)
    grand_total = round(taxable + tax_amount, 2)
    invoice_no = self.next_invoice_no()
    ...
    cur = self.conn.execute(
        """INSERT INTO invoices
           (invoice_no, customer_name, ..., grand_total, payment_mode)
           VALUES (?, ?, ..., ?, ?)""",
        (invoice_no, customer_name, ..., grand_total, payment_mode),
    )
    invoice_id = cur.lastrowid
    for it in items:
        self.conn.execute(
            """INSERT INTO invoice_items
               (invoice_id, product_name, unit_price, quantity, line_total)
               VALUES (?, ?, ?, ?, ?)""",
            (invoice_id, it["name"], it["price"], it["qty"], it["total"]),
        )
        self.adjust_stock(it["name"], -it["qty"])
    self.conn.commit()


def apply_theme(root):
    style = ttk.Style(root)
    style.theme_use("clam")
    root.configure(bg=LIGHT_BG)

    style.configure("Accent.TButton", background=AMBER, foreground=NAVY_DARK,
                    font=("Segoe UI", 10, "bold"), padding=8, borderwidth=0)
    style.map("Accent.TButton", background=[("active", AMBER_DARK)])


class NewBillTab(ttk.Frame):
    def __init__(self, parent, db: Database, on_invoice_created=None):
        super().__init__(parent, style="TFrame", padding=16)
        self.db = db
        self.on_invoice_created = on_invoice_created
        self.cart = [] # list of dicts: name, price, qty, total


def _add_selected_to_cart(self):
    sel = self.product_tree.selection()
    product = self.db.get_product(int(sel[0]))
    qty = self.qty_var.get()

    already_in_cart = sum(i["qty"] for i in self.cart if i["name"] ==
                          product["name"])
    if qty + already_in_cart > product["stock"]:
        messagebox.showwarning(APP_TITLE,
            f"Only {product['stock']} unit(s) of \"{product['name']}\" in stock.")
        return

    for item in self.cart:
        if item["name"] == product["name"]:
            item["qty"] += qty
            item["total"] = round(item["qty"] * item["price"], 2)
            break
    else:
        self.cart.append({"name": product["name"], "price": product["price"],
                          "qty": qty, "total": round(product["price"] * qty, 2)})


for var in (self.discount_var, self.tax_var):
    var.trace_add("write", lambda *a: self._recalc())


def _recalc(self):
    subtotal = sum(i["total"] for i in self.cart)
    discount_amt = round(subtotal * discount_pct / 100, 2)
    taxable = subtotal - discount_amt
    tax_amt = round(taxable * tax_pct / 100, 2)
    grand_total = round(taxable + tax_amt, 2)

    self.subtotal_lbl.set(money(subtotal))
    self.discount_lbl.set(f"- {money(discount_amt)}")
    self.tax_lbl.set(f"+ {money(tax_amt)}")
    self.grand_total_var.set(money(grand_total))


def _generate_bill(self):
    if not self.cart:
        messagebox.showwarning(APP_TITLE, "Cart is empty. Add at least one product.")
        return

    invoice = self.db.create_invoice(
        customer_name=name, customer_phone=phone, items=self.cart,
        discount_percent=discount_pct, tax_percent=tax_pct,
        payment_mode=self.payment_mode_var.get(),
    )
    show_invoice_preview(self, invoice)
    self._new_bill()
    if self.on_invoice_created:
        self.on_invoice_created()


self.tree.bind("<<TreeviewSelect>>", self._on_select)

def _on_select(self, _event=None):
    sel = self.tree.selection()
    if not sel:
        return
    p = self.db.get_product(int(sel[0]))
    self.selected_id = p["id"]
    self.name_var.set(p["name"])
    self.category_var.set(p["category"])
    self.price_var.set(p["price"])
    self.stock_var.set(p["stock"])


def _validated_fields(self):
    name = self.name_var.get().strip()
    if not name:
        messagebox.showwarning(APP_TITLE, "Product name is required.")
        return None
    try:
        price = float(self.price_var.get())
        stock = int(self.stock_var.get())
    except (tk.TclError, ValueError):
        messagebox.showwarning(APP_TITLE, "Price and stock must be numeric.")
        return None
    if price < 0 or stock < 0:
        messagebox.showwarning(APP_TITLE, "Price and stock cannot be negative.")
        return None
    return name, self.category_var.get().strip(), self.unit_var.get().strip() or "pcs", price, stock


def get_invoice(self, invoice_id):
    inv = self.conn.execute(
        "SELECT * FROM invoices WHERE id = ?", (invoice_id,)
    ).fetchone()
    items = self.conn.execute(
        "SELECT * FROM invoice_items WHERE invoice_id = ?", (invoice_id,)
    ).fetchall()
    return inv, items


def _view_selected(self):
    inv_row, items = self.db.get_invoice(int(sel[0]))
    invoice = {
        "invoice_no": inv_row["invoice_no"],
        "items": [{"name": i["product_name"], "price": i["unit_price"],
                   "qty": i["quantity"], "total": i["line_total"]} for i in items],
        "grand_total": inv_row["grand_total"],
        # ...other fields
    }
    show_invoice_preview(self, invoice)


def today_summary(self):
    today = datetime.date.today().strftime("%Y-%m-%d")
    row = self.conn.execute(
        "SELECT COUNT(*) AS cnt, COALESCE(SUM(grand_total), 0) AS total "
        "FROM invoices WHERE invoice_date LIKE ?", (f"{today}%",)
    ).fetchone()
    return row["cnt"], row["total"]


def refresh(self):
    cnt_today, total_today = self.db.today_summary()
    cnt_all, total_all = self.db.all_time_summary()
    low = self.db.low_stock()
    self.card_vars["today_sales"].set(money(total_today))
    self.card_vars["today_invoices"].set(str(cnt_today))
    # ...populate recent_tree and low_tree the same way


def show_invoice_preview(parent, invoice):
    win = tk.Toplevel(parent)
    win.title(f"Invoice {invoice['invoice_no']}")
    win.geometry("480x640")
    ...
    win.transient(parent)
    win.grab_set()


def _format_text_receipt(invoice):
    W = 42
    lines = []
    lines.append(COMPANY_NAME.center(W))
    lines.append("=" * W)
    lines.append(f"{'Item':<20}{'Qty':>5}{'Total':>17}")
    for it in invoice["items"]:
        name = it["name"][:20]
        lines.append(f"{name:<20}{it['qty']:>5}{money(it['total']):>17}")
    ...
    return "\n".join(lines)


def _export_pdf(invoice, path):
    doc = SimpleDocTemplate(path, pagesize=A5, ...)
    elements = [
        Paragraph(COMPANY_NAME, title_style),
        Paragraph(COMPANY_ADDRESS, small_grey),
    ]
    data = [["Item", "Price", "Qty", "Total"]]
    for it in invoice["items"]:
        data.append([it["name"], pdf_money(it["price"]), str(it["qty"]),
                     pdf_money(it["total"])])
    item_table = Table(data, colWidths=["46%", "20%", "12%", "22%"])
    item_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(NAVY)),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ]))
    elements.append(item_table)
    doc.build(elements)


class BillingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1180x720")
        apply_theme(self)
        self.db = Database()
        self._build_header()
        self._build_tabs()

if __name__ == "__main__":
    app = BillingApp()
    app.mainloop()


def _build_tabs(self):
    notebook = ttk.Notebook(self)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    self.dashboard_tab = DashboardTab(notebook, self.db)
    self.new_bill_tab = NewBillTab(notebook, self.db,
                                   on_invoice_created=self._on_data_changed)
    self.products_tab = ProductsTab(notebook, self.db,
                                    on_change=self._on_data_changed)
    self.history_tab = HistoryTab(notebook, self.db)

    notebook.add(self.dashboard_tab, text=" Dashboard ")
    notebook.add(self.new_bill_tab, text=" New Bill ")
    ...


def _on_data_changed(self):
    self.dashboard_tab.refresh()
    self.history_tab.refresh()
    self.products_tab.refresh()
    self.new_bill_tab.refresh_products()
