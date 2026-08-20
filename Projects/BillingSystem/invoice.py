import tkinter as tk
from tkinter import ttk


def show_invoice(parent, invoice):
    window = tk.Toplevel(parent)
    window.title(f"Invoice - {invoice['invoice_no']}")
    window.geometry("500x600")

    text = tk.Text(window, font=("Consolas", 10), padx=15, pady=15)
    text.pack(fill="both", expand=True)

    lines = [
        "           SIMPLE BILLING SYSTEM",
        "=" * 48,
        f"Invoice No : {invoice['invoice_no']}",
        f"Date       : {invoice['invoice_date']}",
        f"Customer   : {invoice['customer_name'] or 'Walk-in'}",
        f"Phone      : {invoice['customer_phone'] or '-'}",
        f"Payment    : {invoice['payment_mode']}",
        "-" * 48,
        f"{'Item':<22}{'Qty':>5}{'Total':>15}",
        "-" * 48,
    ]

    for item in invoice["items"]:
        lines.append(
            f"{item['name'][:22]:<22}{item['qty']:>5}{item['total']:>15.2f}"
        )

    lines += [
        "-" * 48,
        f"{'Subtotal':<32}{invoice['subtotal']:>15.2f}",
        f"{'Discount':<32}{invoice['discount']:>15.2f}",
        f"{'GST (5%)':<32}{invoice['tax']:>15.2f}",
        "=" * 48,
        f"{'GRAND TOTAL':<32}{invoice['grand_total']:>15.2f}",
        "=" * 48,
    ]

    text.insert("1.0", "\n".join(lines))
    text.configure(state="disabled")

    ttk.Button(window, text="Close", command=window.destroy).pack(pady=8)
