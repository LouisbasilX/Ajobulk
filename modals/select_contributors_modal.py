# modals/select_contributors_modal.py
import tkinter as tk
from tkinter import messagebox
from .base_modal import BaseModal
from base_window import BG_CARD, TEXT_WHITE, BTN_GREEN, BTN_RED
import backend_logic as db

class SelectContributorsModal(BaseModal):
    def __init__(self, parent, stock_id, on_selected=None):
        super().__init__(parent, "SELECT CONTRIBUTORS", width=500, height=450, resizable=True)
        self.stock_id = stock_id
        self.on_selected = on_selected
        # Get already existing contributor member IDs
        existing_contributions = db.get_stock_contributions(stock_id)
        self.existing_member_ids = {c['member_id'] for c in existing_contributions}
        self.all_members = db.get_all_members()
        # Filter out members already in this stock
        self.available_members = [m for m in self.all_members if m['member_id'] not in self.existing_member_ids]
        self.filtered_members = self.available_members[:]
        self.check_vars = {}
        self._build_ui()
        self._render_member_list()

    def _build_ui(self):
        # Search bar
        search_frame = tk.Frame(self.modal, bg=BG_CARD)
        search_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(search_frame, text="Enter name/phone_no", bg=BG_CARD, fg=TEXT_WHITE).pack(side="left")
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", self._on_search)

        # Top buttons
        btn_frame = tk.Frame(self.modal, bg=BG_CARD)
        btn_frame.pack(fill="x", padx=10, pady=5)
        self.add_btn = tk.Button(btn_frame, text="+ ADD", bg=BTN_GREEN, fg="white",
                                 command=self._open_add_member, padx=10, cursor="hand2")
        self.add_btn.pack(side="left")
        self.select_all_btn = tk.Button(btn_frame, text="select all", command=self._toggle_select_all)
        self.select_all_btn.pack(side="left", padx=10)

        # Scrollable list of members
        canvas = tk.Canvas(self.modal, bg=BG_CARD, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.modal, orient="vertical", command=canvas.yview)
        self.list_frame = tk.Frame(canvas, bg=BG_CARD)
        self.list_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.list_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        scrollbar.pack(side="right", fill="y")

        # Buttons at bottom
        bottom_frame = tk.Frame(self.modal, bg=BG_CARD)
        bottom_frame.pack(fill="x", pady=10)
        tk.Button(bottom_frame, text="CANCEL", bg=BTN_RED, fg="white",
                  command=self.modal.destroy, padx=10).pack(side="right", padx=5)
        tk.Button(bottom_frame, text="CONFIRM", bg=BTN_GREEN, fg="white",
                  command=self._confirm, padx=10).pack(side="right", padx=5)

    def _on_search(self, event):
        term = self.search_entry.get().strip().lower()
        if not term:
            self.filtered_members = self.available_members[:]
        else:
            self.filtered_members = [m for m in self.available_members
                                     if term in m['fullname'].lower() or term in m['phone_number']]
        self._render_member_list()

    def _render_member_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        self.check_vars.clear()
        for member in self.filtered_members:
            var = tk.BooleanVar()
            self.check_vars[member['member_id']] = var
            row = tk.Frame(self.list_frame, bg=BG_CARD)
            row.pack(fill="x", pady=2)
            cb = tk.Checkbutton(row, variable=var, bg=BG_CARD)
            cb.pack(side="left")
            name_label = tk.Label(row, text=f"{member['fullname']}", bg=BG_CARD, fg=TEXT_WHITE,
                                  font=("Arial", 10, "bold"))
            name_label.pack(side="left", padx=5)
            phone_label = tk.Label(row, text=f"📞 {member['phone_number']}", bg=BG_CARD, fg="gray")
            phone_label.pack(side="left", padx=5)

    def _toggle_select_all(self):
        select = not any(var.get() for var in self.check_vars.values())
        for var in self.check_vars.values():
            var.set(select)

    def _open_add_member(self):
        self._create_new_member_modal()

    def _create_new_member_modal(self):
        modal = tk.Toplevel(self.modal)
        modal.title("Add New Member")
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
                # Refresh member list
                self.all_members = db.get_all_members()
                # Find newly added member
                new_member = None
                for m in self.all_members:
                    if m['fullname'] == name and m['phone_number'] == phone:
                        new_member = m
                        break
                if new_member and new_member['member_id'] not in self.existing_member_ids:
                    # Add to available_members
                    self.available_members.append(new_member)
                    self.filtered_members = self.available_members[:]
                    self._render_member_list()
                    # Auto-select this new member
                    if new_member['member_id'] in self.check_vars:
                        self.check_vars[new_member['member_id']].set(True)
                messagebox.showinfo("Success", f"Member {name} created. Select it and confirm.")
                modal.destroy()
        tk.Button(modal, text="SAVE", bg=BTN_GREEN, command=save).pack(pady=10)

    def _confirm(self):
        selected_ids = [mid for mid, var in self.check_vars.items() if var.get()]
        if not selected_ids:
            messagebox.showwarning("No selection", "Please select at least one member.")
            return
        # Ensure we don't add duplicates
        new_ids = [mid for mid in selected_ids if mid not in self.existing_member_ids]
        if not new_ids:
            messagebox.showinfo("Info", "Selected members already contributors.")
            self.modal.destroy()
            return
        if self.on_selected:
            self.on_selected(new_ids)
        self.modal.destroy()