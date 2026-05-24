# modals/edit_contribution_modal.py
import tkinter as tk
from tkinter import messagebox
from .base_modal import BaseModal
from base_window import BG_CARD, TEXT_WHITE, BTN_RED, BTN_GREEN
import backend_logic as db

class EditContributionModal(BaseModal):
    def __init__(self, parent, contribution_id, member_name, current_amount, on_success=None):
        super().__init__(parent, "EDIT CONTRIBUTION", width=400, height=220)
        self.contribution_id = contribution_id
        self.member_name = member_name
        self.current_amount = current_amount
        self.on_success = on_success
        self._build_ui()

    def _build_ui(self):
        self.modal.grid_columnconfigure(0, weight=1)
        self.modal.grid_columnconfigure(1, weight=2)

        tk.Label(self.modal, text="EDIT CONTRIBUTION", font=("Arial", 12, "bold"),
                 bg=BG_CARD, fg=TEXT_WHITE).grid(row=0, column=0, columnspan=2, pady=10)
        tk.Label(self.modal, text=self.member_name, font=("Arial", 10),
                 bg=BG_CARD, fg=TEXT_WHITE).grid(row=1, column=0, columnspan=2, pady=5)

        self.make_label("CONTRIBUTION (₦)", row=2, column=0, padx=10, pady=5)
        self.amount_entry = self.make_entry(row=2, column=1, padx=10, pady=5)
        self.amount_entry.insert(0, self.current_amount)

        # Buttons frame
        btn_frame = tk.Frame(self.modal, bg=BG_CARD)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        self.make_button_in_frame(btn_frame, "CANCEL", self.modal.destroy, BTN_RED)
        self.make_button_in_frame(btn_frame, "SAVE", self._save, BTN_GREEN)

    def make_button_in_frame(self, parent, text, command, bg_color):
        btn = tk.Button(parent, text=text, bg=bg_color, fg="white",
                        font=("Arial", 10, "bold"), command=command,
                        padx=15, pady=5, cursor="hand2", relief="flat")
        btn.pack(side="right", padx=10)

    def _save(self):
        new_amount = self.amount_entry.get().strip()
        if not new_amount:
            messagebox.showerror("Error", "Amount required")
            return
        try:
            new_amount = int(new_amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number")
            return
        try:
            db.edit_contribution(self.contribution_id, new_amount)
            messagebox.showinfo("Success", "Contribution updated")
            if self.on_success:
                self.on_success()
            self.modal.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update: {str(e)}")