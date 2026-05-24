# modals/edit_org_modal.py
import tkinter as tk
from tkinter import messagebox
from .base_modal import BaseModal
from base_window import BG_CARD, TEXT_WHITE, BTN_RED, BTN_GREEN
import backend_logic as db

class EditOrgModal(BaseModal):
    def __init__(self, parent, org_id, current_name, on_success=None):
        super().__init__(parent, "EDIT ORGANIZATION", width=400, height=220)
        self.org_id = org_id
        self.current_name = current_name
        self.on_success = on_success
        self._build_ui()

    def _build_ui(self):
        self.modal.grid_columnconfigure(0, weight=1)
        self.modal.grid_columnconfigure(1, weight=2)

        # Show current name as label
        tk.Label(self.modal, text=self.current_name, font=("Arial", 12, "bold"),
                 bg=BG_CARD, fg=TEXT_WHITE).grid(row=0, column=0, columnspan=2, pady=10)

        self.make_label("NAME", row=1, column=0, padx=5, pady=5)
        self.name_entry = self.make_entry(row=1, column=1, padx=5, pady=5)
        self.name_entry.insert(0, self.current_name)

        tk.Label(self.modal, text="ex: Ajo women", font=("Arial", 9),
                 bg=BG_CARD, fg="gray").grid(row=2, column=1, sticky="w", padx=5)

        # Buttons frame – ensures visibility
        btn_frame = tk.Frame(self.modal, bg=BG_CARD)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        self.make_button_in_frame(btn_frame, "CANCEL", self.modal.destroy, BTN_RED)
        self.make_button_in_frame(btn_frame, "SAVE", self._save, BTN_GREEN)

    def make_button_in_frame(self, parent, text, command, bg_color):
        btn = tk.Button(parent, text=text, bg=bg_color, fg="white",
                        font=("Arial", 10, "bold"), command=command,
                        padx=20, pady=5, cursor="hand2", relief="flat")
        btn.pack(side="right", padx=10)

    def _save(self):
        new_name = self.name_entry.get().strip()
        if not new_name:
            messagebox.showerror("Error", "Name cannot be empty")
            return
        if new_name == self.current_name:
            self.modal.destroy()
            return
        db.edit_org_name(self.org_id, new_name)
        messagebox.showinfo("Success", "Organization updated")
        if self.on_success:
            self.on_success()
        self.modal.destroy()