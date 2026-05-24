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
        self._load_data()

    def _build_ui(self):
        top = tk.Frame(self, bg=self.BG_MAIN)
        top.pack(fill="x", padx=40, pady=(30,10))

        self.stock_title = tk.Label(top, text="", font=self.app.font_heading,
                                    bg=self.BG_MAIN, fg=TEXT_WHITE)
        self.stock_title.pack(anchor="w")

        self.breadcrumb_frame = tk.Frame(top, bg=self.BG_MAIN)
        self.breadcrumb_frame.pack(anchor="w", fill="x", pady=(5, 0))

        stats_frame = tk.Frame(self, bg=self.BG_MAIN)
        stats_frame.pack(fill="x", padx=40, pady=(10,20))

        self.card_quantity = self.app.make_stat_card(stats_frame, "QUANTITY", 0)
        self.card_contributors = self.app.make_stat_card(stats_frame, "CONTRIBUTORS", 0)
        self.card_reached = self.app.make_stat_card(stats_frame, "TARGET REACHED", "0%")
        self.card_quantity.pack(side="left", padx=5)
        self.card_contributors.pack(side="left", padx=5)
        self.card_reached.pack(side="left", padx=5)

        contrib_row = tk.Frame(self, bg=self.BG_MAIN)
        contrib_row.pack(fill="x", padx=40, pady=(0,10))
        self.contributed_label = tk.Label(contrib_row, text="CONTRIBUTED: ₦ 0 / 0",
                                          font=self.app.font_body, bg=self.BG_MAIN, fg=TEXT_WHITE)
        self.contributed_label.pack(side="left")
        self.edit_stock_btn = self.app.make_button(contrib_row, "Edit", BTN_BLUE,
                                                   command=self._edit_stock, width=6)
        self.edit_stock_btn.pack(side="right")

        self.app.make_button(self, "+ ADD CONTRIBUTOR", BTN_GREEN,
                             command=self._open_add_contributor).pack(anchor="w", padx=40, pady=(0,10))
        self.app.make_section_label(self, "CONTRIBUTOR STATUS").pack(anchor="w", padx=40, pady=(0,10))

        search_row = tk.Frame(self, bg=self.BG_MAIN)
        search_row.pack(fill="x", padx=40, pady=(0,10))
        tk.Label(search_row, text="Enter name", font=self.app.font_body,
                 bg=self.BG_MAIN, fg=TEXT_LIGHT).pack(side="left")
        self.search_entry = tk.Entry(search_row, textvariable=self._search_var, width=30)
        self.search_entry.pack(side="left", padx=5)
        self.export_btn = self.app.make_button(search_row, "EXPORT PDF", BTN_PURPLE,
                                               command=self._export_report, width=12)
        self.export_btn.pack(side="right")

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

        nav_frame = tk.Frame(table_nav_frame, bg=self.BG_MAIN)
        nav_frame.pack(side="right", anchor="n", padx=(10,0), pady=20)
        self.app.make_nav_arrows(nav_frame,
                                 up_cmd=self._scroll_up,
                                 down_cmd=self._scroll_down).pack()

    def _load_data(self):
        self.stock = db.get_record("stocks.csv", self.stock_id)
        if not self.stock:
            messagebox.showerror("Error", "Stock not found")
            self.app.show_frame("DashboardFrame")
            return
        self.org = db.get_record("organizations.csv", self.stock['org_id'])
        self.contributions = db.get_stock_contributions(self.stock_id)
        self._filter_contributions()
        self._update_stats()
        self._update_breadcrumb()
        add_quick_link(self.stock_id, self.stock['product_name'], self.org['name'])
        self.app.load_quick_links_from_json()

    def _update_breadcrumb(self):
        for widget in self.breadcrumb_frame.winfo_children():
            widget.destroy()

        from dashboard_frame import DashboardFrame
        from org_frame import OrgFrame

        home = tk.Label(self.breadcrumb_frame, text="Home", font=self.app.font_body,
                        fg=TEXT_LIGHT, bg=self.BG_MAIN, cursor="hand2")
        home.pack(side="left")
        home.bind("<Button-1>", lambda e: self.app.show_frame(DashboardFrame))

        tk.Label(self.breadcrumb_frame, text=" > ", font=self.app.font_body,
                 fg=TEXT_LIGHT, bg=self.BG_MAIN).pack(side="left")

        org_link = tk.Label(self.breadcrumb_frame, text=self.org['name'],
                            font=self.app.font_body, fg=TEXT_LIGHT,
                            bg=self.BG_MAIN, cursor="hand2")
        org_link.pack(side="left")
        org_link.bind("<Button-1>",
                      lambda e: self.app.show_frame(OrgFrame, org_id=self.org['org_id']))

        tk.Label(self.breadcrumb_frame, text=" > ", font=self.app.font_body,
                 fg=TEXT_LIGHT, bg=self.BG_MAIN).pack(side="left")

        tk.Label(self.breadcrumb_frame, text=self.stock['product_name'],
                 font=self.app.font_body, fg=TEXT_WHITE,
                 bg=self.BG_MAIN).pack(side="left")

    def _update_stats(self):
        target_qty = int(self.stock['target_quantity'])
        contributed = float(self.stock['contributed_amount'])
        price = float(self.stock['estimated_price'])
        total_target_value = price
        percent = (contributed / total_target_value * 100) if total_target_value > 0 else 0

        self.card_quantity.winfo_children()[1].config(text=str(target_qty))
        self.card_contributors.winfo_children()[1].config(text=str(len(self.contributions)))
        self.card_reached.winfo_children()[1].config(text=f"{percent:.0f}%")
        self.contributed_label.config(
            text=f"CONTRIBUTED: ₦ {contributed:.2f} / {total_target_value:.2f}")
        self.stock_title.config(text=self.stock['product_name'].upper())

    def _filter_contributions(self):
        term = self._search_var.get().strip().lower()
        if not term:
            self._filtered = self.contributions.copy()
        else:
            self._filtered = []
            for c in self.contributions:
                member = db.get_record("members.csv", c['member_id'])
                if member and (term in member['fullname'].lower()
                               or term in member['phone_number']):
                    self._filtered.append(c)
        self._page = 0
        self._render_contributors()

    def _render_contributors(self):
        for widget in self.rows_container.winfo_children():
            widget.destroy()

        page_size = 5
        start = self._page * page_size
        visible = self._filtered[start:start+page_size]

        for contrib in visible:
            member = db.get_record("members.csv", contrib['member_id'])
            if not member:
                continue
            row = tk.Frame(self.rows_container, bg=BG_CARD, pady=4)
            row.pack(fill="x", pady=2)

            tk.Label(row, text=contrib['member_id'], width=5,
                     bg=BG_CARD, fg=TEXT_WHITE).pack(side="left", padx=5)
            tk.Label(row, text=member['fullname'], width=25,
                     bg=BG_CARD, fg=TEXT_WHITE, anchor="w").pack(side="left", padx=5)
            tk.Label(row, text=f"₦ {contrib['amount_paid']}", width=15,
                     bg=BG_CARD, fg=TEXT_WHITE).pack(side="left", padx=5)

            btn_frame = tk.Frame(row, bg=BG_CARD)
            btn_frame.pack(side="left", padx=5)
            self.app.make_button(btn_frame, "EDIT", BTN_BLUE,
                                 command=lambda c=contrib: self._edit_contribution(c),
                                 width=6).pack(side="left", padx=2)
            self.app.make_button(btn_frame, "REMOVE", BTN_RED,
                                 command=lambda c=contrib: self._remove_contribution(c),
                                 width=6).pack(side="left", padx=2)

    def _scroll_up(self):
        if self._page > 0:
            self._page -= 1
            self._render_contributors()

    def _scroll_down(self):
        page_size = 5
        max_page = max(0, (len(self._filtered)-1)//page_size)
        if self._page < max_page:
            self._page += 1
            self._render_contributors()

    def _edit_stock(self):
        def refresh():
            self._load_data()
        EditStockModal(self, self.stock_id, self.stock, on_success=refresh)

    def _open_add_contributor(self):
        def refresh():
            self._load_data()
        AddContributorModal(self, self.stock_id, on_contributors_added=refresh)

    def _edit_contribution(self, contrib):
        member = db.get_record("members.csv", contrib['member_id'])
        def refresh():
            self._load_data()
        EditContributionModal(self, contrib['contribution_id'], member['fullname'],
                              contrib['amount_paid'], on_success=refresh)

    def _remove_contribution(self, contrib):
        if messagebox.askyesno("Remove Contribution", "Remove this contributor's payment?"):
            db.delete_contribution(contrib['contribution_id'])
            self._load_data()

    def _export_report(self):
        try:
            db.export_stock_report(self.stock_id)
            messagebox.showinfo("Export", f"Report exported to {db.get_record('settings.csv','1')['export_path']}")
        except Exception as e:
            messagebox.showerror("Export Error", str(e))