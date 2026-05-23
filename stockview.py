# stock_frame.py
import tkinter as tk
from tkinter import messagebox
from base_window import BaseFrame, BTN_GREEN, BTN_BLUE, BTN_RED, BG_CARD, TEXT_WHITE, TEXT_LIGHT, BTN_PURPLE
import backend_logic as db
from modals import EditStockModal, AddContributorModal, EditContributionModal
from settings_manager import add_quick_link

class StockFrame(BaseFrame):
    def __init__(self, parent, controller, stock_id):
        super().__init__(parent, controller)
        self.stock_id = stock_id
        self.stock = None
        self.org = None
        self.contributions = []
        self._filtered = []
        self._page = 0
        self._search_var = tk.StringVar()
        self._build_ui()

    def _build_ui(self):
        # Top bar: stock name and breadcrumb
        top = tk.Frame(self, bg=self.BG_MAIN)
        top.pack(fill="x", padx=40, pady=(30,10))

        self.stock_title = tk.Label(top, text="", font=self.app.font_heading,
                                    bg=self.BG_MAIN, fg=TEXT_WHITE)
        self.stock_title.pack(anchor="w")

        self.breadcrumb_frame = tk.Frame(top, bg=self.BG_MAIN)
        self.breadcrumb_frame.pack(anchor="w", fill="x", pady=(5, 0))

        # Stats row
        stats_frame = tk.Frame(self, bg=self.BG_MAIN)
        stats_frame.pack(fill="x", padx=40, pady=(10,20))

        self.card_quantity = self.app.make_stat_card(stats_frame, "QUANTITY", 0)
        self.card_contributors = self.app.make_stat_card(stats_frame, "CONTRIBUTORS", 0)
        self.card_reached = self.app.make_stat_card(stats_frame, "TARGET REACHED", "0%")
        self.card_quantity.pack(side="left", padx=5)
        self.card_contributors.pack(side="left", padx=5)
        self.card_reached.pack(side="left", padx=5)

        # Contribution bar and edit button
        contrib_row = tk.Frame(self, bg=self.BG_MAIN)
        contrib_row.pack(fill="x", padx=40, pady=(0,10))
        self.contributed_label = tk.Label(contrib_row, text="CONTRIBUTED: ₦ 0 / 0",
                                          font=self.app.font_body, bg=self.BG_MAIN, fg=TEXT_WHITE)
        self.contributed_label.pack(side="left")
        self.edit_stock_btn = self.app.make_button(contrib_row, "Edit", BTN_BLUE,
                                                   command=self._edit_stock, width=6)
        self.edit_stock_btn.pack(side="right")

    def _load_data(self):
        pass