# modals/add_contributor_modal.py
import tkinter as tk
from tkinter import messagebox
from .base_modal import BaseModal
from .select_contributors_modal import SelectContributorsModal
from base_window import BG_CARD, TEXT_WHITE, BTN_BLUE, BTN_GREEN, BTN_RED
import backend_logic as db

class AddContributorModal(BaseModal):
    def __init__(self, parent, stock_id, on_contributors_added=None):
        super().__init__(parent, "ADD CONTRIBUTORS", width=400, height=200)
        self.stock_id = stock_id
        self.on_contributors_added = on_contributors_added
        self._build_ui()

    def _build_ui(self):
        tk.Label(self.modal, text="SELECT FROM", font=("Arial", 12, "bold"),
                 bg=BG_CARD, fg=TEXT_WHITE).pack(pady=10)

        btn_frame = tk.Frame(self.modal, bg=BG_CARD)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="EXISTING MEMBERS", bg=BTN_BLUE, fg="white",
                  command=self._choose_existing, padx=20, pady=5).pack(side="left", padx=10)
        tk.Button(btn_frame, text="NEW MEMBER", bg=BTN_GREEN, fg="white",
                  command=self._create_new_member, padx=20, pady=5).pack(side="left", padx=10)

        tk.Button(self.modal, text="CANCEL", bg=BTN_RED, fg="white",
                  command=self.modal.destroy, padx=10).pack(pady=20)

    def _choose_existing(self):
        def on_selected(member_ids):
            if member_ids:
                db.add_contributions(self.stock_id, member_ids)
                messagebox.showinfo("Success", f"{len(member_ids)} contributor(s) added.")
                if self.on_contributors_added:
                    self.on_contributors_added()
            self.modal.destroy()
        # Create a new instance of SelectContributorsModal
        SelectContributorsModal(self.modal, self.stock_id, on_selected=on_selected)

    def _create_new_member(self):
        # Simple form to create a single member and add as contributor
        modal = tk.Toplevel(self.modal)
        modal.title("New Member")
        modal.geometry("350x200")
        modal.configure(bg=BG_CARD)
        modal.transient(self.modal)
        modal.grab_set()
        tk.Label(modal, text="Full Name", bg=BG_CARD, fg=TEXT_WHITE).pack(pady=5)
        name_entry = tk.Entry(modal)
        name_entry.pack()
        tk.Label(modal, text="Phone Number", bg=BG_CARD, fg=TEXT_WHITE).pack(pady=5)
        phone_entry = tk.Entry(modal)
        phone_entry.pack()
        def save():
            name = name_entry.get().strip()
            phone = phone_entry.get().strip()
            if not name or not phone:
                messagebox.showerror("Error", "Both fields required")
                return
            res = db.create_member(name, phone)
            if "Error" in res:
                messagebox.showerror("Error", res)
            else:
                # Get the newly created member
                members = db.get_all_members()
                new_member = None
                for m in members:
                    if m['fullname'] == name and m['phone_number'] == phone:
                        new_member = m
                        break
                if new_member:
                    db.add_contributions(self.stock_id, [new_member['member_id']])
                    messagebox.showinfo("Success", f"Member {name} added as contributor.")
                    if self.on_contributors_added:
                        self.on_contributors_added()
                else:
                    messagebox.showinfo("Success", "Member created. Please refresh and add manually.")
                modal.destroy()
                self.modal.destroy()
        tk.Button(modal, text="SAVE", bg=BTN_GREEN, command=save).pack(pady=10)