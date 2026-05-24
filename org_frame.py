# org_frame.py
import tkinter as tk
from tkinter import messagebox
from base_window import BaseFrame, BTN_GREEN, BTN_BLUE, BTN_RED, BG_CARD, TEXT_WHITE, TEXT_LIGHT
import backend_logic as db
from modals import CreateStockModal, EditOrgModal, AddContributorModal

class OrgFrame(BaseFrame):
    def __init__(self, parent, controller, org_id):
        super().__init__(parent, controller)
        self.org_id = org_id
        self.org_data = None
        self.stocks = []
        self._page = 0
        self._build_ui()
        self._load_data()

    def _build_ui(self):
        # Top bar with org name and breadcrumb
        top_frame = tk.Frame(self, bg=self.BG_MAIN)
        top_frame.pack(fill="x", padx=40, pady=(40, 10))

        self.org_title = tk.Label(top_frame, text="", font=self.app.font_heading,
                                  bg=self.BG_MAIN, fg=TEXT_WHITE)
        self.org_title.pack(anchor="w")

        # Clickable breadcrumb frame (replaces static label)
        self.breadcrumb_frame = tk.Frame(top_frame, bg=self.BG_MAIN)
        self.breadcrumb_frame.pack(anchor="w", fill="x", pady=(5, 0))

        # Stats row
        stats_frame = tk.Frame(self, bg=self.BG_MAIN)
        stats_frame.pack(fill="x", padx=40, pady=(10, 20))

        self.card_stocks = self.app.make_stat_card(stats_frame, "STOCKS", 0)
        self.card_members = self.app.make_stat_card(stats_frame, "INVOLVED MEMBERS", 0)
        self.card_stocks.pack(side="left", padx=5)
        self.card_members.pack(side="left", padx=5)

        self.edit_btn = self.app.make_button(stats_frame, "EDIT", BTN_BLUE,
                                             command=self._edit_org, width=8)
        self.edit_btn.pack(side="right")

        # New stock button
        self.app.make_button(self, "+ NEW STOCK", BTN_GREEN,
                             command=self._open_create_stock).pack(anchor="w", padx=40, pady=(0, 10))

        # Stocks list header
        self.app.make_section_label(self, "STOCKS").pack(anchor="w", padx=40, pady=(0, 10))

        # List container with navigation
        list_row = tk.Frame(self, bg=self.BG_MAIN)
        list_row.pack(fill="both", expand=True, padx=40, pady=(0, 20))

        self.list_container = tk.Frame(list_row, bg=self.BG_MAIN)
        self.list_container.pack(side="left", fill="both", expand=True)

        self.app.make_nav_arrows(
            list_row,
            up_cmd=self._scroll_up,
            down_cmd=self._scroll_down
        ).pack(side="right", anchor="n", padx=(10,0), pady=4)

    def _load_data(self):
        self.org_data = db.get_org_metrics(self.org_id)
        if not self.org_data:
            messagebox.showerror("Error", "Organization not found")
            self.app.show_frame("DashboardFrame")
            return
        self.org_title.config(text=self.org_data['name'].upper())
        self.stocks = db.get_org_stocks(self.org_id)
        self._update_stats()
        self._render_stock_list()
        self._update_breadcrumb()   # new: rebuild clickable breadcrumb

    def _update_breadcrumb(self):
       """Rebuild clickable breadcrumb: Home > Organization Name"""
       from dashboard_frame import DashboardFrame   # Import class, not string
    
       for widget in self.breadcrumb_frame.winfo_children():
        widget.destroy()

       # Home link
       home = tk.Label(self.breadcrumb_frame, text="Home", font=self.app.font_body,
                    fg=TEXT_LIGHT, bg=self.BG_MAIN, cursor="hand2")
       home.pack(side="left")
       home.bind("<Button-1>", lambda e: self.app.show_frame(DashboardFrame))

       # Separator
       sep = tk.Label(self.breadcrumb_frame, text=" > ", font=self.app.font_body,
                   fg=TEXT_LIGHT, bg=self.BG_MAIN)
       sep.pack(side="left")

       # Current organization (not clickable)
       org_label = tk.Label(self.breadcrumb_frame, text=self.org_data['name'], font=self.app.font_body,
                         fg=TEXT_WHITE, bg=self.BG_MAIN)
       org_label.pack(side="left")
   
    def _update_stats(self):
        self.card_stocks.winfo_children()[1].config(text=str(len(self.stocks)))
        self.card_members.winfo_children()[1].config(text=str(self.org_data.get('MEMBERS_INVOLVED', 0)))

    def _render_stock_list(self):
        for widget in self.list_container.winfo_children():
            widget.destroy()

        page_size = 3
        start = self._page * page_size
        visible = self.stocks[start:start+page_size]

        for stock in visible:
            self._make_stock_card(stock)

    def _make_stock_card(self, stock):
        card = tk.Frame(self.list_container, bg=BG_CARD, pady=12, padx=20)
        card.pack(fill="x", pady=6)

        # Stock name
        tk.Label(card, text=stock['product_name'].upper(), font=self.app.font_heading,
                 bg=BG_CARD, fg=TEXT_WHITE).pack(anchor="w")

        # Bottom row: stats and buttons
        bottom = tk.Frame(card, bg=BG_CARD)
        bottom.pack(fill="x", pady=(8,0))

        # Left info: contributors count, created date (placeholder)
        contributors = len(db.get_stock_contributions(stock['stock_id']))
        tk.Label(bottom, text=f"👥 {contributors} contributors", font=self.app.font_body,
                 bg=BG_CARD, fg=TEXT_LIGHT).pack(side="left")
        tk.Label(bottom, text=f"📅 created nov,2019", font=self.app.font_body,
                 bg=BG_CARD, fg=TEXT_LIGHT).pack(side="left", padx=20)

        # Buttons: OPEN and DELETE
        self.app.make_button(bottom, "OPEN", BTN_BLUE,
                             command=lambda s=stock: self._open_stock(s),
                             width=8).pack(side="right", padx=(6,0))
        self.app.make_button(bottom, "DELETE", BTN_RED,
                             command=lambda s=stock: self._delete_stock(s),
                             width=8).pack(side="right")

    def _scroll_up(self):
        if self._page > 0:
            self._page -= 1
            self._render_stock_list()

    def _scroll_down(self):
        page_size = 3
        max_page = max(0, (len(self.stocks)-1)//page_size)
        if self._page < max_page:
            self._page += 1
            self._render_stock_list()

    def _edit_org(self):
        from modals import EditOrgModal
        def refresh():
            self._load_data()
        EditOrgModal(self, self.org_id, self.org_data['name'], on_success=refresh)

    def _open_create_stock(self):
        def refresh():
            self._load_data()
        from modals import CreateStockModal
        CreateStockModal(self, self.org_id, on_success=refresh)

    def _open_stock(self, stock):
        from stock_frame import StockFrame
        self.app.show_frame(StockFrame, stock_id=stock['stock_id'])

    def _delete_stock(self, stock):
        if messagebox.askyesno("Delete Stock", f"Delete stock '{stock['product_name']}'?\nAll contributions will be deleted."):
            db.delete_stock(stock['stock_id'])
            self._load_data()