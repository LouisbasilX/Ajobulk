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
        self._search_var.trace_add("write", lambda *args: self._filter_contributions())
        self._build_ui()

    def _build_ui(self):
        # Top bar
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

        # Add contributor button
        self.app.make_button(self, "+ ADD CONTRIBUTOR", BTN_GREEN,
                             command=self._open_add_contributor).pack(anchor="w", padx=40, pady=(0,10))

        # Contributors section header
        self.app.make_section_label(self, "CONTRIBUTOR STATUS").pack(anchor="w", padx=40, pady=(0,10))

        # Search bar and Export button row
        search_row = tk.Frame(self, bg=self.BG_MAIN)
        search_row.pack(fill="x", padx=40, pady=(0,10))
        tk.Label(search_row, text="Enter name", font=self.app.font_body,
                 bg=self.BG_MAIN, fg=TEXT_LIGHT).pack(side="left")
        self.search_entry = tk.Entry(search_row, textvariable=self._search_var, width=30)
        self.search_entry.pack(side="left", padx=5)
        self.export_btn = self.app.make_button(search_row, "EXPORT PDF", BTN_PURPLE,
                                               command=self._export_report, width=12)
        self.export_btn.pack(side="right")

        # Table headers
        list_container = tk.Frame(self, bg=self.BG_MAIN)
        list_container.pack(fill="both", expand=True, padx=40, pady=(0,20))

        header_frame = tk.Frame(list_container, bg=BG_CARD, height=30)
        header_frame.pack(fill="x", pady=(0,5))
        tk.Label(header_frame, text="ID", width=5, bg=BG_CARD,
                 fg=TEXT_WHITE, font=self.app.font_body).pack(side="left", padx=5)
        tk.Label(header_frame, text="NAME", width=25, bg=BG_CARD,
                 fg=TEXT_WHITE, font=self.app.font_body).pack(side="left", padx=5)
        tk.Label(header_frame, text="AMOUNT", width=15, bg=BG_CARD,
                 fg=TEXT_WHITE, font=self.app.font_body).pack(side="left", padx=5)
        tk.Label(header_frame, text="UPDATE / REMOVE", width=20, bg=BG_CARD,
                 fg=TEXT_WHITE, font=self.app.font_body).pack(side="left", padx=5)

        # Scrollable canvas
        table_nav_frame = tk.Frame(list_container, bg=self.BG_MAIN)
        table_nav_frame.pack(fill="both", expand=True)

        canvas_frame = tk.Frame(table_nav_frame, bg=self.BG_MAIN)
        canvas_frame.pack(side="left", fill="both", expand=True)

        canvas = tk.Canvas(canvas_frame, bg=self.BG_MAIN, highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        self.rows_container = tk.Frame(canvas, bg=self.BG_MAIN)
        self.rows_container.bind("<Configure>",
                                 lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=self.rows_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Nav arrows
        nav_frame = tk.Frame(table_nav_frame, bg=self.BG_MAIN)
        nav_frame.pack(side="right", anchor="n", padx=(10,0), pady=20)
        self.app.make_nav_arrows(nav_frame,
                                 up_cmd=self._scroll_up,
                                 down_cmd=self._scroll_down).pack()

    def _load_data(self):
        pass

    def _filter_contributions(self):
        pass

    def _render_contributors(self):
        pass

    def _scroll_up(self):
        pass

    def _scroll_down(self):
        pass

    def _edit_stock(self):
        pass

    def _open_add_contributor(self):
        pass

    def _export_report(self):
        pass