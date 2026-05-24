# modals/create_stock_modal.py
import tkinter as tk
from tkinter import messagebox
from .base_modal import BaseModal
from base_window import BG_CARD, BTN_RED, BTN_GREEN
import backend_logic as db

class CreateStockModal(BaseModal):
    def __init__(self, parent, org_id, on_success=None):
        super().__init__(parent, "CREATE STOCK", width=450, height=420)
        self.org_id = org_id
        self.on_success = on_success
        self._build_ui()

    def _build_ui(self):
        self.modal.grid_columnconfigure(0, weight=1)
        self.modal.grid_columnconfigure(1, weight=2)

        row = 0
        self.make_label("NAME", row=row, column=0, padx=5, pady=5)
        self.name_entry = self.make_entry(row=row, column=1, padx=5, pady=5)
        tk.Label(self.modal, text="ex: oil", font=("Arial", 9),
                 bg=BG_CARD, fg="gray").grid(row=row+1, column=1, sticky="w", padx=5)
        row += 2

        self.make_label("UNIT", row=row, column=0, padx=5, pady=5)
        self.unit_entry = self.make_entry(row=row, column=1, padx=5, pady=5)
        self.unit_entry.insert(0, "Kg")
        tk.Label(self.modal, text="ex: Kg, Litres, Pieces", font=("Arial", 9),
                 bg=BG_CARD, fg="gray").grid(row=row+1, column=1, sticky="w", padx=5)
        row += 2

        self.make_label("TARGET QUANTITY", row=row, column=0, padx=5, pady=5)
        self.qty_entry = self.make_entry(row=row, column=1, padx=5, pady=5)
        self.qty_entry.insert(0, "100")
        tk.Label(self.modal, text="ex: 100", font=("Arial", 9),
                 bg=BG_CARD, fg="gray").grid(row=row+1, column=1, sticky="w", padx=5)
        row += 2

        self.make_label("TARGET PRICE (₦)", row=row, column=0, padx=5, pady=5)
        self.price_entry = self.make_entry(row=row, column=1, padx=5, pady=5)
        self.price_entry.insert(0, "10000")
        tk.Label(self.modal, text="ex: 10000", font=("Arial", 9),
                 bg=BG_CARD, fg="gray").grid(row=row+1, column=1, sticky="w", padx=5)
        row += 2

        # Buttons – use grid, not pack
        btn_frame = tk.Frame(self.modal, bg=BG_CARD)
        btn_frame.grid(row=row, column=0, columnspan=2, pady=20)
        self.make_button_in_frame(btn_frame, "CANCEL", self.modal.destroy, BTN_RED)
        self.make_button_in_frame(btn_frame, "SAVE", self._create, BTN_GREEN)

    def make_button_in_frame(self, parent, text, command, bg_color):
        btn = tk.Button(parent, text=text, bg=bg_color, fg="white",
                        font=("Arial", 10, "bold"), command=command,
                        padx=15, pady=5, cursor="hand2", relief="flat")
        btn.pack(side="right", padx=10)

    def _create(self):
        name = self.name_entry.get().strip()
        unit = self.unit_entry.get().strip()
        qty = self.qty_entry.get().strip()
        price = self.price_entry.get().strip()
        if not name or not unit or not qty or not price:
            messagebox.showerror("Error", "All fields are required")
            return
        try:
            qty = int(qty)
            price = float(price)
        except ValueError:
            messagebox.showerror("Error", "Quantity must be integer, price a number")
            return
        res = db.add_stock(name, self.org_id, unit, qty, price)
        if "Error" in res:
            messagebox.showerror("Error", res)
        else:
            messagebox.showinfo("Success", res)
            if self.on_success:
                self.on_success()
            self.modal.destroy()