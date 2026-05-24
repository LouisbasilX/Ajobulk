# members_frame.py
import tkinter as tk
from tkinter import messagebox
from base_window import BaseFrame, BTN_GREEN, BTN_BLUE, BTN_RED, BG_CARD, TEXT_WHITE, TEXT_LIGHT
from backend_logic import get_all_records, create_member, edit_member, delete_member

class MembersFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self._page = 0
        self._members = []
        self._filtered_members = []
        self._search_var = tk.StringVar()
        self._search_var.trace_add("write", lambda *args: self._on_search())
        self._build_ui()
        self._load_data()

    def _build_ui(self):
        # Top bar with stat card and add button
        top = tk.Frame(self, bg=self.BG_MAIN)
        top.pack(fill="x", padx=40, pady=(40, 0))

        self.card_members = self.app.make_stat_card(top, "MEMBERS", 0)
        self.card_members.pack(side="left", padx=10)

        self.app.make_button(top, "+ ADD MEMBER", BTN_GREEN, command=self._open_add_member).pack(side="right", padx=10)

        # Search bar
        search_frame = tk.Frame(self, bg=self.BG_MAIN)
        search_frame.pack(fill="x", padx=40, pady=(20, 10))

        tk.Label(search_frame, text="Enter name/phone", font=self.app.font_body, bg=self.BG_MAIN, fg=TEXT_LIGHT).pack(side="left")
        self.search_entry = tk.Entry(search_frame, textvariable=self._search_var, font=self.app.font_body, width=30)
        self.search_entry.pack(side="left", padx=10)

        # Section label
        self.app.make_section_label(self, "MEMBERS").pack(anchor="w", padx=40, pady=(10, 10))

        # List container with navigation
        list_row = tk.Frame(self, bg=self.BG_MAIN)
        list_row.pack(fill="both", expand=True, padx=40, pady=(0, 20))

        self.list_container = tk.Frame(list_row, bg=self.BG_MAIN)
        self.list_container.pack(side="left", fill="both", expand=True)

        self.app.make_nav_arrows(
            list_row,
            up_cmd=self._scroll_up,
            down_cmd=self._scroll_down
        ).pack(side="right", anchor="n", padx=(10, 0), pady=4)

    def _load_data(self):
        self._members = get_all_records("members.csv")
        self._apply_filter()

    def _apply_filter(self):
        search_term = self._search_var.get().strip().lower()
        if not search_term:
            self._filtered_members = self._members.copy()
        else:
            self._filtered_members = [
                m for m in self._members
                if search_term in m['fullname'].lower() or search_term in m['phone_number']
            ]
        self._page = 0
        self._render_member_list()
        self._update_stat_card()

    def _on_search(self):
        self._apply_filter()

    def _update_stat_card(self):
        total = len(self._filtered_members)
        self.card_members.winfo_children()[1].config(text=str(total))

    def _render_member_list(self):
        # Clear container
        for widget in self.list_container.winfo_children():
            widget.destroy()

        page_size = 5
        start = self._page * page_size
        visible = self._filtered_members[start:start + page_size]

        for member in visible:
            self._make_member_card(member)

    def _make_member_card(self, member):
        card = tk.Frame(self.list_container, bg=BG_CARD, pady=16, padx=24)
        card.pack(fill="x", pady=8)

        # Name
        tk.Label(
            card,
            text=member['fullname'],
            font=self.app.font_heading,
            bg=BG_CARD, fg=TEXT_WHITE
        ).pack(anchor="w")

        # Bottom row: phone + buttons
        bottom = tk.Frame(card, bg=BG_CARD)
        bottom.pack(fill="x", pady=(10, 0))

        # Phone number
        tk.Label(
            bottom,
            text=f"📞  {member['phone_number']}",
            font=self.app.font_body,
            bg=BG_CARD, fg=TEXT_LIGHT
        ).pack(side="left")

        # Buttons: EDIT and REMOVE
        self.app.make_button(
            bottom, "EDIT", BTN_BLUE,
            command=lambda m=member: self._edit_member(m),
            width=8
        ).pack(side="right", padx=(6, 0))

        self.app.make_button(
            bottom, "REMOVE", BTN_RED,
            command=lambda m=member: self._remove_member(m),
            width=8
        ).pack(side="right")

    def _scroll_up(self):
        if self._page > 0:
            self._page -= 1
            self._render_member_list()

    def _scroll_down(self):
        page_size = 5
        max_page = max(0, (len(self._filtered_members) - 1) // page_size)
        if self._page < max_page:
            self._page += 1
            self._render_member_list()

    def _open_add_member(self):
        self._open_member_modal()

    def _edit_member(self, member):
        self._open_member_modal(member)

    def _open_member_modal(self, member=None):
        modal = tk.Toplevel(self)
        modal.title("Edit Member" if member else "Add Member")
        modal.geometry("400x300")
        modal.configure(bg=BG_CARD)
        modal.transient(self)
        modal.grab_set()

        # Center on parent
        x = self.winfo_x() + (self.winfo_width() // 2) - 200
        y = self.winfo_y() + (self.winfo_height() // 2) - 150
        modal.geometry(f"+{x}+{y}")

        # Form fields
        tk.Label(modal, text="Full Name:", bg=BG_CARD, fg=TEXT_WHITE, font=self.app.font_body).pack(pady=(20, 5))
        name_entry = tk.Entry(modal, font=self.app.font_body, width=30)
        name_entry.pack()

        tk.Label(modal, text="Phone Number:", bg=BG_CARD, fg=TEXT_WHITE, font=self.app.font_body).pack(pady=(10, 5))
        phone_entry = tk.Entry(modal, font=self.app.font_body, width=30)
        phone_entry.pack()

        if member:
            name_entry.insert(0, member['fullname'])
            phone_entry.insert(0, member['phone_number'])

        def save():
            name = name_entry.get().strip()
            phone = phone_entry.get().strip()
            if not name or not phone:
                messagebox.showerror("Error", "Both fields are required")
                return

            if member:
                result = edit_member(member['member_id'], name, phone)
            else:
                result = create_member(name, phone)

            if result and "Error" in result:
                messagebox.showerror("Error", result)
            else:
                modal.destroy()
                self._load_data()  # refresh

        btn_frame = tk.Frame(modal, bg=BG_CARD)
        btn_frame.pack(pady=20)
        self.app.make_button(btn_frame, "Save", BTN_GREEN, command=save, width=12).pack(side="left", padx=5)
        self.app.make_button(btn_frame, "Cancel", BTN_RED, command=modal.destroy, width=12).pack(side="left", padx=5)

    def _remove_member(self, member):
        if messagebox.askyesno("Confirm Delete", f"Delete member '{member['fullname']}'?\nThis will also remove all their contributions."):
            delete_member(member['member_id'])
            self._load_data()