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

    def _build_ui(self):
        pass

    def _load_data(self):
        pass