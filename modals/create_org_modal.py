# modals/create_org_modal.py
import tkinter as tk
from tkinter import messagebox
from .base_modal import BaseModal
from base_window import BG_CARD, BTN_RED, BTN_GREEN
import backend_logic as db

class CreateOrgModal(BaseModal):
    def __init__(self, parent, on_success=None):
        super().__init__(parent, "CREATE ORGANIZATION", width=400, height=200)
        self.on_success = on_success
        self._build_ui()

    def _build_ui(self):
        self.modal.grid_columnconfigure(0, weight=1)
        self.modal.grid_columnconfigure(1, weight=2)

        self.make_label("NAME", row=0, column=0, padx=5, pady=5)
        self.name_entry = self.make_entry(row=0, column=1, padx=5, pady=5)
        tk.Label(self.modal, text="ex: ajo traders", font=("Arial", 9),
                 bg=BG_CARD, fg="gray").grid(row=1, column=1, sticky="w", padx=5)

        # Buttons frame for better alignment
        btn_frame = tk.Frame(self.modal, bg=BG_CARD)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=15)
        self.make_button("CANCEL", self.modal.destroy, btn_frame, bg_color=BTN_RED, side="right", padx=10)
        self.make_button("SAVE", self._create, btn_frame, bg_color=BTN_GREEN, side="right", padx=10)

    def make_button(self, text, command, parent, bg_color, side="right", padx=5):
        btn = tk.Button(parent, text=text, bg=bg_color, fg="white",
                        font=("Arial", 10, "bold"), command=command,
                        padx=15, pady=5, cursor="hand2", relief="flat")
        btn.pack(side=side, padx=padx)

    def _create(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Name is required")
            return
        res = db.add_organization(name)
        if "Error" in res:
            messagebox.showerror("Error", res)
        else:
            messagebox.showinfo("Success", res)
            if self.on_success:
                self.on_success()
            self.modal.destroy()