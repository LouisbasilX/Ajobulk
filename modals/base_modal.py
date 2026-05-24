# modals/base_modal.py
import tkinter as tk
from base_window import BG_CARD, TEXT_WHITE, BTN_GREEN, BTN_RED, BTN_BLUE

class BaseModal:
    def __init__(self, parent, title, width=450, height=300, resizable=False):
        self.parent = parent
        self.modal = tk.Toplevel(parent)
        self.modal.title(title)
        self.modal.configure(bg=BG_CARD)
        self.modal.geometry(f"{width}x{height}")
        self.modal.transient(parent)
        self.modal.grab_set()
        self.modal.resizable(resizable, resizable)
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (width // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (height // 2)
        self.modal.geometry(f"+{x}+{y}")

    def make_label(self, text, row, column=0, padx=10, pady=5, sticky="e"):
        lbl = tk.Label(self.modal, text=text, font=("Arial", 10, "bold"),
                       bg=BG_CARD, fg=TEXT_WHITE)
        lbl.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)

    def make_entry(self, row, column=1, padx=10, pady=5, width=30):
        entry = tk.Entry(self.modal, font=("Arial", 10), width=width)
        entry.grid(row=row, column=column, padx=padx, pady=pady, sticky="w")
        return entry