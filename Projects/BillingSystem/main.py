import tkinter as tk
from tkinter import ttk

from database import Database
from billing import BillingService, BillingFrame
from products import ProductsFrame
from history import HistoryFrame
from dashboard import DashboardFrame


class BillingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Billing System")
        self.geometry("1100x680")
        self.minsize(950, 600)

        self.db = Database()
        self.service = BillingService(self.db)

        self.setup_style()
        self.build_ui()

    def setup_style(self):
        style = ttk.Style(self)
        
        style.theme_use("xpnative")
        
        style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"))
        style.configure("Heading.TLabel", font=("Segoe UI", 14, "bold"))
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))
        style.configure("Treeview", rowheight=28)

    def build_ui(self):
        header = ttk.Frame(self, padding=15)
        header.pack(fill="x")
        ttk.Label(header, text="Jaiswal Electronics", style="Title.TLabel").pack(side="left")

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self.dashboard = DashboardFrame(notebook, self.service)
        self.billing = BillingFrame(notebook, self.service, )
        self.products = ProductsFrame(notebook, self.service)
        self.history = HistoryFrame(notebook, self.service)

        notebook.add(self.dashboard, text=" Dashboard ")
        notebook.add(self.billing, text=" New Bill ")
        notebook.add(self.products, text=" Products ")
        notebook.add(self.history, text=" History ")

        # self.refresh_all()

    # def refresh_all(self):
    #     self.products.refresh_products()
    #     self.billing.refresh_products()
    #     self.history.refresh_history()
    #     self.dashboard.refresh_dashboard()

    def destroy(self):
        self.db.close()
        super().destroy()


if __name__ == "__main__":
    app = BillingApp()
    app.mainloop()
