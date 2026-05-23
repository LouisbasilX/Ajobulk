# dashboard_frame.py
import tkinter as tk
from base_window import BaseFrame, BTN_GREEN, BTN_BLUE, BTN_RED, BG_CARD, TEXT_WHITE, TEXT_LIGHT
from modals.create_org_modal import CreateOrgModal
from settings_manager import get_quick_links

class DashboardFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self._page = 0
        self._orgs = []
        self._build_ui()
        self._load_data()

    def _build_ui(self):
        top = tk.Frame(self, bg=self.BG_MAIN)
        top.pack(fill="x", padx=40, pady=(40,0))
        self.card_orgs = self.app.make_stat_card(top, "ORGANIZATIONS", 0)
        self.card_bulks = self.app.make_stat_card(top, "ACTIVE BULKS", 0)
        self.card_members = self.app.make_stat_card(top, "MEMBERS", 0)

        self.card_orgs.pack(side="left", padx=10)
        self.card_bulks.pack(side="left", padx=10)
        self.card_members.pack(side="left", padx=10)
        self.app.make_button(top, "+ NEW ORGANIZATION", BTN_GREEN, command=self._open_create_org).pack(side="right", padx=10)

        # Quick Links section
        self.app.make_section_label(self, "QUICK LINKS").pack(anchor="w", padx=40, pady=(20,10))
        self.quick_links_frame = tk.Frame(self, bg=self.BG_MAIN)
        self.quick_links_frame.pack(fill="x", padx=40, pady=(0,20))

        self.app.make_section_label(self, "ORGANIZATIONS").pack(anchor='w', padx=40, pady=(10,10))

        list_row = tk.Frame(self, bg=self.BG_MAIN)
        list_row.pack(fill="both", expand=True, padx=40, pady=(0,20))

        self.list_container = tk.Frame(list_row, bg=self.BG_MAIN)
        self.list_container.pack(side="left", fill="both", expand=True)

        self.app.make_nav_arrows(list_row, up_cmd=self._scroll_up, down_cmd=self._scroll_down
        ).pack(side="right", anchor="n", padx=(10,0), pady=4)

    def _load_data(self):
        from backend_logic import get_dashboard_metrics, get_all_orgs
        metrics = get_dashboard_metrics()
        self._orgs = get_all_orgs()
        self.card_orgs.winfo_children()[1].config(text=metrics["ORGANIZATIONS"])
        self.card_bulks.winfo_children()[1].config(text=metrics["ACTIVE BULKS"])
        self.card_members.winfo_children()[1].config(text=metrics["MEMBERS"])
        self._render_org_list()
        self._load_quick_links()
        self.app.load_quick_links_from_json()
        
    def _load_quick_links(self):
        for widget in self.quick_links_frame.winfo_children():
            widget.destroy()
        links = get_quick_links()
        if not links:
            tk.Label(self.quick_links_frame, text="No recent stocks. Open a stock from an organization.",
                     font=self.app.font_body, bg=self.BG_MAIN, fg=TEXT_LIGHT).pack()
            return
        for link in links:
            from stock_frame import StockFrame
            btn = self.app.make_button(
                self.quick_links_frame,
                f"{link['stock_name']} ({link['org_name']})",
                BTN_BLUE,
                command=lambda s=link['stock_id']: self.app.show_frame(StockFrame, stock_id=s),
                width=25
            )
            btn.pack(side="left", padx=5)

    def _render_org_list(self):
        for widget in self.list_container.winfo_children():
            widget.destroy()
        page_size = 2
        start = self._page * page_size
        visible_orgs = self._orgs[start:start+page_size]
        for org in visible_orgs:
            self._make_org_card(org)

    def _make_org_card(self, org):
        card = tk.Frame(self.list_container, bg=BG_CARD, pady=16, padx=24)
        card.pack(fill="x", pady=8)
        tk.Label(card, text=org["name"].upper(), font=self.app.font_heading, bg=BG_CARD, fg=TEXT_WHITE).pack(anchor="w")
        bottom = tk.Frame(card, bg=BG_CARD)
        bottom.pack(fill="x", pady=(10,0))
        tk.Label(bottom, text=f"👥  {org['member_count']} members", font=self.app.font_body, bg=BG_CARD, fg=TEXT_LIGHT).pack(side="left")
        tk.Label(bottom, text=f"📋  Founded {org['date_founded']}", font=self.app.font_body, bg=BG_CARD, fg=TEXT_LIGHT).pack(side="left", padx=24)
        self.app.make_button(bottom, "OPEN", BTN_BLUE, command=lambda o=org: self._open_org(o), width=10).pack(side="right", padx=(6,0))
        self.app.make_button(bottom, "DELETE", BTN_RED, command=lambda o=org: self._delete_org(o), width=10).pack(side="right")

   

    def _open_create_org(self):
        CreateOrgModal(self, on_success=self._load_data)

    def _open_org(self, org):
        from org_frame import OrgFrame
        self.app._highlight_nav("dashboard")
        self.app.show_frame(OrgFrame, org_id=org["id"])

    def _delete_org(self, org):
        from backend_logic import delete_org
        delete_org(org["id"])
        self._load_data()