import tkinter as tk
from tkinter import font as tkfont

# ═══════════════════════════════════════════════════════════════
#  COLOUR PALETTE
# ═══════════════════════════════════════════════════════════════
BG_MAIN        = "#1a1a1a"
BG_SIDEBAR     = "#111111"
BG_SIDEBAR_EXP = "#181818"   # expanded sidebar bg (slightly lighter)
BG_CARD        = "#2a2a2a"
BG_CARD_ALT    = "#2d2d3a"
BG_INPUT       = "#2e2e2e"
BG_ACTIVE      = "#252525"
BG_LOGO        = "#000000"

BTN_GREEN      = "#1a6b2a"
BTN_BLUE       = "#1a3a7a"
BTN_GOLD       = "#7a5500"
BTN_RED        = "#8b0000"
BTN_PURPLE     = "#6a3fa0"

TEXT_WHITE     = "#ffffff"
TEXT_GREY      = "#888888"
TEXT_LIGHT     = "#cccccc"
TEXT_BLUE_LINK = "#5588ff"
TEXT_RED_LINK  = "#ff4444"
TEXT_LABEL     = "#aaaaaa"

SIDEBAR_W_OPEN  = 220
SIDEBAR_W_CLOSE = 70

# ═══════════════════════════════════════════════════════════════
#  NAV ITEMS  — (display_text, nav_key, emoji_icon)
#  Using high-quality Unicode symbols that render crisply in Tk
# ═══════════════════════════════════════════════════════════════
NAV_ITEMS = [
    ("DASHBOARD", "dashboard", "🏠"),
    ("MEMBERS",   "members",   "👥"),
    ("SETTINGS",  "settings",  "⚙"),
]


# ═══════════════════════════════════════════════════════════════
#  ROOT APP WINDOW
# ═══════════════════════════════════════════════════════════════
class AjobulkApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Ajobulk")
        self.geometry("1440x1024")
        self.minsize(900, 600)
        self.configure(bg=BG_MAIN)
        self.resizable(True, True)

        # crisp rendering hints
        self.tk.call("tk", "scaling", 1.0)

        self._setup_fonts()

        self.sidebar_open   = True
        self._active_key    = "dashboard"
        self._nav_rows      = {}   # key → (icon_lbl, text_lbl, row_frame)
        self.current_frame  = None
        self.context        = {}

        # quick-access links stored as (stock_name, org_name) tuples
        self._quick_links   = []
        self._quick_frames  = []

        self._build_layout()
        self.load_quick_links_from_json()
    # ───────────────────────────────────────────────────────────
    #  FONTS  — use Liberation Sans (clean Linux equivalent of Arial)
    # ───────────────────────────────────────────────────────────
    def _setup_fonts(self):
        def F(family, size, *style):
            return tkfont.Font(family=family, size=size, weight=style[0] if style else "normal")

        base = "Liberation Sans"
        self.font_logo    = F(base, 13, "bold")
        self.font_nav     = F(base, 11, "bold")
        self.font_icon    = F("Segoe UI Emoji", 16)   # emoji font
        self.font_title   = F(base, 20, "bold")
        self.font_heading = F(base, 13, "bold")
        self.font_body    = F(base, 11)
        self.font_small   = F(base, 9)
        self.font_btn     = F(base, 11, "bold")
        self.font_stat    = F(base, 30, "bold")
        self.font_label   = F(base, 9,  "bold")
        self.font_quick   = F(base, 10, "bold")
        self.font_breadcrumb = F(base, 10)
        self.font_heading_large = ("Arial", 18, "bold")
        self.font_body_bold = ("Arial", 10, "bold")
    # ───────────────────────────────────────────────────────────
    #  LAYOUT
    # ───────────────────────────────────────────────────────────
    def _build_layout(self):
        # Sidebar panel
        self.sidebar_panel = tk.Frame(
            self, bg=BG_SIDEBAR, width=SIDEBAR_W_OPEN
        )
        self.sidebar_panel.pack(side="left", fill="y")
        self.sidebar_panel.pack_propagate(False)

        # Content area
        self.content_area = tk.Frame(self, bg=BG_MAIN)
        self.content_area.pack(side="left", fill="both", expand=True)

        self._build_sidebar_contents()

    # ───────────────────────────────────────────────────────────
    #  SIDEBAR CONTENTS
    # ───────────────────────────────────────────────────────────
    def _build_sidebar_contents(self):
        sb = self.sidebar_panel

        # ── Toggle button (top-right of sidebar) ──────────────
        self.toggle_btn = tk.Button(
            sb,
            text="◀",
            font=tkfont.Font(family="Liberation Sans", size=10),
            bg=BG_SIDEBAR, fg=TEXT_GREY,
            activebackground=BG_ACTIVE, activeforeground=TEXT_WHITE,
            relief="flat", bd=0, cursor="hand2",
            command=self._toggle_sidebar,
        )
        self.toggle_btn.pack(anchor="ne", padx=10, pady=(12, 0))

        # ── Logo block ────────────────────────────────────────
        self.logo_frame = tk.Frame(sb, bg=BG_SIDEBAR)
        self.logo_frame.pack(fill="x", padx=14, pady=(8, 28))

        # circular logo circle (canvas trick for crisp circle)
        self.logo_canvas = tk.Canvas(
            self.logo_frame, width=52, height=52,
            bg=BG_SIDEBAR, highlightthickness=0,
        )
        self.logo_canvas.pack(side="left")
        self.logo_canvas.create_oval(2, 2, 50, 50, fill=BG_LOGO, outline="#333333", width=1)
        self.logo_canvas.create_text(26, 26, text="📦", font=tkfont.Font(family="Segoe UI Emoji", size=18), fill=TEXT_WHITE)

        self.logo_text_lbl = tk.Label(
            self.logo_frame,
            text="AJO BULK",
            font=self.font_logo,
            bg=BG_SIDEBAR, fg=TEXT_WHITE,
        )
        self.logo_text_lbl.pack(side="left", padx=10)

        # ── Nav items ─────────────────────────────────────────
        self.nav_container = tk.Frame(sb, bg=BG_SIDEBAR)
        self.nav_container.pack(fill="x", pady=(0, 0))

        for label, key, icon in NAV_ITEMS:
            self._make_nav_row(self.nav_container, label, key, icon)

        # ── Divider ───────────────────────────────────────────
        self.divider = tk.Frame(sb, bg="#2a2a2a", height=1)
        self.divider.pack(fill="x", padx=14, pady=(24, 16))

        # ── Quick Access ──────────────────────────────────────
        self.quick_header = tk.Label(
            sb,
            text="QUICK ACCESS",
            font=self.font_label,
            bg=BG_SIDEBAR, fg=TEXT_GREY,
        )
        self.quick_header.pack(anchor="w", padx=20, pady=(0, 10))

        self.quick_container = tk.Frame(sb, bg=BG_SIDEBAR)
        self.quick_container.pack(fill="x", padx=20)

        # Highlight first nav item by default
        self._highlight_nav("dashboard")

    def _make_nav_row(self, parent, label, key, icon):
        """Build one icon + label nav row."""
        row = tk.Frame(parent, bg=BG_SIDEBAR, cursor="hand2", pady=0)
        row.pack(fill="x", padx=8, pady=2)

        # Active indicator bar (left edge)
        indicator = tk.Frame(row, bg=BG_SIDEBAR, width=3)
        indicator.pack(side="left", fill="y")

        # Icon label
        icon_lbl = tk.Label(
            row,
            text=icon,
            font=self.font_icon,
            bg=BG_SIDEBAR, fg=TEXT_GREY,
            width=3,
            anchor="center",
        )
        icon_lbl.pack(side="left", padx=(6, 4), pady=10)

        # Text label
        text_lbl = tk.Label(
            row,
            text=label,
            font=self.font_nav,
            bg=BG_SIDEBAR, fg=TEXT_GREY,
            anchor="w",
        )
        text_lbl.pack(side="left", pady=10)

        # Click bindings on every widget in the row
        for widget in (row, indicator, icon_lbl, text_lbl):
            widget.bind("<Button-1>", lambda e, k=key: self._sidebar_click(k))
            widget.bind("<Enter>",    lambda e, r=row, i=icon_lbl, t=text_lbl: self._nav_hover(r, i, t, True))
            widget.bind("<Leave>",    lambda e, k=key, r=row, i=icon_lbl, t=text_lbl: self._nav_hover_leave(k, r, i, t))

        self._nav_rows[key] = (icon_lbl, text_lbl, row, indicator)

    def _nav_hover(self, row, icon_lbl, text_lbl, entering):
        if entering:
            row.config(bg=BG_ACTIVE)
            icon_lbl.config(bg=BG_ACTIVE, fg=TEXT_WHITE)
            text_lbl.config(bg=BG_ACTIVE, fg=TEXT_WHITE)

    def _nav_hover_leave(self, key, row, icon_lbl, text_lbl):
        if key != self._active_key:
            row.config(bg=BG_SIDEBAR)
            icon_lbl.config(bg=BG_SIDEBAR, fg=TEXT_GREY)
            text_lbl.config(bg=BG_SIDEBAR, fg=TEXT_GREY)

    def _highlight_nav(self, key):
        for k, (icon_lbl, text_lbl, row, indicator) in self._nav_rows.items():
            if k == key:
                row.config(bg=BG_ACTIVE)
                icon_lbl.config(bg=BG_ACTIVE, fg=TEXT_WHITE)
                text_lbl.config(bg=BG_ACTIVE, fg=TEXT_WHITE)
                indicator.config(bg=BTN_GREEN)
            else:
                row.config(bg=BG_SIDEBAR)
                icon_lbl.config(bg=BG_SIDEBAR, fg=TEXT_GREY)
                text_lbl.config(bg=BG_SIDEBAR, fg=TEXT_GREY)
                indicator.config(bg=BG_SIDEBAR)
        self._active_key = key

    def _sidebar_click(self, key):
        self._highlight_nav(key)
        self.event_generate(f"<<Nav-{key}>>")

    # ───────────────────────────────────────────────────────────
    #  SIDEBAR TOGGLE
    # ───────────────────────────────────────────────────────────
    def _toggle_sidebar(self):
        self.sidebar_open = not self.sidebar_open

        if self.sidebar_open:
            # expand
            self.sidebar_panel.config(width=SIDEBAR_W_OPEN)
            self.toggle_btn.config(text="◀")
            # show text labels and extras
            self.logo_text_lbl.pack(side="left", padx=10)
            for key, (icon_lbl, text_lbl, row, indicator) in self._nav_rows.items():
                text_lbl.pack(side="left", pady=10)
            self.divider.pack(fill="x", padx=14, pady=(24, 16))
            self.quick_header.pack(anchor="w", padx=20, pady=(0, 10))
            self.quick_container.pack(fill="x", padx=20)
        else:
            # collapse — hide text, keep icons
            self.sidebar_panel.config(width=SIDEBAR_W_CLOSE)
            self.toggle_btn.config(text="▶")
            self.logo_text_lbl.pack_forget()
            for key, (icon_lbl, text_lbl, row, indicator) in self._nav_rows.items():
                text_lbl.pack_forget()
            self.divider.pack_forget()
            self.quick_header.pack_forget()
            self.quick_container.pack_forget()

    # ───────────────────────────────────────────────────────────
    #  QUICK ACCESS LINKS
    # ───────────────────────────────────────────────────────────
    def add_quick_link(self, display_text, callback):
        """Add a blue link under QUICK ACCESS. Call from any frame."""
        lbl = tk.Label(
            self.quick_container,
            text=display_text.upper(),
            font=self.font_quick,
            bg=BG_SIDEBAR, fg=TEXT_BLUE_LINK,
            cursor="hand2", anchor="w",
        )
        lbl.pack(fill="x", pady=4)
        lbl.bind("<Button-1>", lambda e: callback())
        self._quick_frames.append(lbl)

    def clear_quick_links(self):
        for lbl in self._quick_frames:
            lbl.destroy()
        self._quick_frames.clear()

    def load_quick_links_from_json(self):
      """Load quick links from app_settings.json and populate sidebar."""
      from settings_manager import get_quick_links
      from stock_frame import StockFrame
      self.clear_quick_links()
      
      for link in get_quick_links():
        
        # Create callback that opens the stock
        def make_callback(stock_id):
            return lambda: self.show_frame(StockFrame, stock_id=stock_id)
        self.add_quick_link(
            f"{link['stock_name']} ({link['org_name']})",
            make_callback(link['stock_id'])
        )

    # ───────────────────────────────────────────────────────────
    #  FRAME / MODAL MANAGEMENT
    # ───────────────────────────────────────────────────────────
    def show_frame(self, FrameClass, **kwargs):
        if self.current_frame is not None:
            self.current_frame.destroy()
        frame = FrameClass(self.content_area, controller=self, **kwargs)
        frame.pack(fill="both", expand=True)
        self.current_frame = frame

    def open_modal(self, ModalClass, **kwargs):
        modal = ModalClass(self, controller=self, **kwargs)
        modal.grab_set()
        self.wait_window(modal)

    # ───────────────────────────────────────────────────────────
    #  REUSABLE UI PRIMITIVES
    # ───────────────────────────────────────────────────────────
    def make_button(self, parent, text, color, command, width=14, padx=16, pady=8):
        return tk.Button(
            parent,
            text=text,
            font=self.font_btn,
            bg=color, fg=TEXT_WHITE,
            activebackground=color, activeforeground=TEXT_WHITE,
            relief="flat", bd=0,
            padx=padx, pady=pady,
            cursor="hand2",
            width=width,
            command=command,
        )

    def make_entry(self, parent, placeholder="", width=30):
        frame = tk.Frame(parent, bg=BG_INPUT, padx=8, pady=7)
        entry = tk.Entry(
            frame,
            font=self.font_body,
            bg=BG_INPUT, fg=TEXT_LIGHT,
            insertbackground=TEXT_WHITE,
            relief="flat", bd=0,
            highlightthickness=0,
            width=width,
        )
        entry.pack(fill="x")
        _attach_placeholder(entry, placeholder)
        return frame, entry

    def make_stat_card(self, parent, label, value, width=200, height=110):
        card = tk.Frame(parent, bg=BG_CARD, width=width, height=height)
        card.pack_propagate(False)
        tk.Label(card, text=label, font=self.font_label,
                 bg=BG_CARD, fg=TEXT_GREY).pack(pady=(20, 4))
        tk.Label(card, text=str(value), font=self.font_stat,
                 bg=BG_CARD, fg=TEXT_WHITE).pack()
        return card

    def make_section_label(self, parent, text):
        return tk.Label(parent, text=text, font=self.font_heading,
                        bg=BG_MAIN, fg=TEXT_WHITE, anchor="w")

    def make_nav_arrows(self, parent, up_cmd, down_cmd):
        frame = tk.Frame(parent, bg=BG_MAIN)
        for sym, cmd in [("∧", up_cmd), ("∨", down_cmd)]:
            tk.Button(
                frame, text=sym,
                font=tkfont.Font(family="Liberation Sans", size=13, weight="bold"),
                bg=BG_CARD, fg=TEXT_WHITE,
                activebackground=BG_ACTIVE, activeforeground=TEXT_WHITE,
                relief="flat", bd=0, width=3, cursor="hand2",
                command=cmd,
            ).pack(pady=3)
        return frame


# ═══════════════════════════════════════════════════════════════
#  BASE FRAME
# ═══════════════════════════════════════════════════════════════
class BaseFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_MAIN)
        self.controller = controller
        self.app = controller

        # colour shortcuts
        self.BG_MAIN     = BG_MAIN
        self.BG_CARD     = BG_CARD
        self.BG_CARD_ALT = BG_CARD_ALT
        self.BG_INPUT    = BG_INPUT
        self.BTN_GREEN   = BTN_GREEN
        self.BTN_BLUE    = BTN_BLUE
        self.BTN_GOLD    = BTN_GOLD
        self.BTN_RED     = BTN_RED
        self.BTN_PURPLE  = BTN_PURPLE
        self.TEXT_WHITE  = TEXT_WHITE
        self.TEXT_GREY   = TEXT_GREY
        self.TEXT_LIGHT  = TEXT_LIGHT
        self.TEXT_BLUE_LINK = TEXT_BLUE_LINK
        self.TEXT_RED_LINK  = TEXT_RED_LINK
    
 

#  BASE MODAL

class BaseModal(tk.Toplevel):
    MODAL_BG = "#1e1e1e"

    def __init__(self, parent, controller, title_text="", width=520, height=420):
        super().__init__(parent)
        self.controller = controller
        self.app = controller
        self.configure(bg=self.MODAL_BG)
        self.resizable(False, False)
        self.title("")
        self.overrideredirect(False)

        # crisp
        self.tk.call("tk", "scaling", 1.0)

        self._center(parent, width, height)

        if title_text:
            tk.Label(
                self, text=title_text,
                font=tkfont.Font(family="Liberation Sans", size=16, weight="bold"),
                bg=self.MODAL_BG, fg=TEXT_WHITE,
            ).pack(pady=(32, 12))

    def _center(self, parent, w, h):
        self.update_idletasks()
        try:
            px, py = parent.winfo_rootx(), parent.winfo_rooty()
            pw, ph = parent.winfo_width(), parent.winfo_height()
        except Exception:
            px, py, pw, ph = 100, 100, 1440, 1024
        x = px + (pw - w) // 2
        y = py + (ph - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def make_button(self, parent, text, color, command, width=12):
        return tk.Button(
            parent, text=text,
            font=tkfont.Font(family="Liberation Sans", size=11, weight="bold"),
            bg=color, fg=TEXT_WHITE,
            activebackground=color, activeforeground=TEXT_WHITE,
            relief="flat", bd=0, padx=14, pady=10,
            cursor="hand2", width=width, command=command,
        )

    def make_entry(self, parent, placeholder="", width=28):
        frame = tk.Frame(parent, bg=BG_INPUT, padx=8, pady=7)
        entry = tk.Entry(
            frame,
            font=tkfont.Font(family="Liberation Sans", size=11),
            bg=BG_INPUT, fg=TEXT_LIGHT,
            insertbackground=TEXT_WHITE,
            relief="flat", bd=0, highlightthickness=0,
            width=width,
        )
        entry.pack(fill="x")
        _attach_placeholder(entry, placeholder)
        return frame, entry

    def make_field_label(self, parent, text):
        return tk.Label(
            parent, text=text,
            font=tkfont.Font(family="Liberation Sans", size=10, weight="bold"),
            bg=self.MODAL_BG, fg=TEXT_WHITE, anchor="w",
        )


# ═══════════════════════════════════════════════════════════════
#  SHARED HELPER
# ═══════════════════════════════════════════════════════════════
def _attach_placeholder(entry, placeholder):
    if not placeholder:
        return
    entry.insert(0, placeholder)
    entry.config(fg=TEXT_GREY)

    def on_in(e):
        if entry.get() == placeholder:
            entry.delete(0, "end")
            entry.config(fg=TEXT_LIGHT)

    def on_out(e):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg=TEXT_GREY)

    entry.bind("<FocusIn>",  on_in)
    entry.bind("<FocusOut>", on_out)


# ═══════════════════════════════════════════════════════════════
#  SMOKE TEST
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = AjobulkApp()

    # sample quick links to preview sidebar
    app.add_quick_link("Cara Women's Rice", lambda: print("quick link 1"))
    app.add_quick_link("Ajo Market's Oil",  lambda: print("quick link 2"))

    tk.Label(
        app.content_area,
        text="Base shell ✓\nPlug in your frames here.",
        font=tkfont.Font(family="Liberation Sans", size=15),
        bg=BG_MAIN, fg=TEXT_GREY, justify="center",
    ).place(relx=0.5, rely=0.5, anchor="center")

    app.mainloop()