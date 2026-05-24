# settings_frame.py
import tkinter as tk
from tkinter import filedialog, messagebox
from base_window import BaseFrame, BTN_GREEN, BTN_BLUE, BTN_RED, BG_CARD, TEXT_WHITE, TEXT_LIGHT
import backend_logic as db
import os

class SettingsFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self._build_scrollable_ui()
        self._load_all_settings()

    def _build_scrollable_ui(self):
        """Create a canvas with scrollbar for the entire settings view."""
        main_container = tk.Frame(self, bg=self.BG_MAIN)
        main_container.pack(fill="both", expand=True)

        canvas = tk.Canvas(main_container, bg=self.BG_MAIN, highlightthickness=0)
        scrollbar = tk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg=self.BG_MAIN)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def _on_canvas_resize(event):
            canvas.itemconfig(1, width=event.width)
        canvas.bind("<Configure>", _on_canvas_resize)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        self._build_ui()

    def _build_ui(self):
        """Create all sections inside the scrollable frame."""
        # Title – using existing font_heading (no font_heading_large)
        tk.Label(
            self.scrollable_frame,
            text="Settings",
            font=self.app.font_heading,
            bg=self.BG_MAIN, fg=TEXT_WHITE
        ).pack(anchor="w", padx=40, pady=(40, 10))

        # Section label
        self.app.make_section_label(self.scrollable_frame, "SETTINGS").pack(anchor="w", padx=40, pady=(0, 20))

        # ---------- PDF Report Customization Card ----------
        pdf_card = tk.Frame(self.scrollable_frame, bg=BG_CARD, padx=30, pady=20)
        pdf_card.pack(fill="x", padx=40, pady=(0, 20))

        tk.Label(
            pdf_card, text="PDF Report Customization", font=self.app.font_heading,
            bg=BG_CARD, fg=TEXT_WHITE
        ).pack(anchor="w", pady=(0, 20))

        # Business Name
        tk.Label(pdf_card, text="BUSINESS NAME", font=self.app.font_body, bg=BG_CARD, fg=TEXT_LIGHT).pack(anchor="w")
        self.biz_name_entry = tk.Entry(pdf_card, font=self.app.font_body, width=50)
        self.biz_name_entry.pack(anchor="w", pady=(5, 5))
        # Use font_body instead of font_body_small
        tk.Label(pdf_card, text="Ex: Ajo Enterprise", font=self.app.font_body, bg=BG_CARD, fg=TEXT_LIGHT).pack(anchor="w", pady=(0, 15))

        # Delivery Note
        tk.Label(pdf_card, text="DELIVERY NOTE", font=self.app.font_body, bg=BG_CARD, fg=TEXT_LIGHT).pack(anchor="w")
        self.delivery_note_text = tk.Text(pdf_card, font=self.app.font_body, width=50, height=4, wrap="word")
        self.delivery_note_text.pack(anchor="w", pady=(5, 5))
        tk.Label(pdf_card, text="Ex: Please bring your own sacks for collection.", font=self.app.font_body, bg=BG_CARD, fg=TEXT_LIGHT).pack(anchor="w", pady=(0, 15))

        self.app.make_button(pdf_card, "SAVE", BTN_GREEN, command=self._save_pdf_settings, width=15).pack(anchor="w")

        # ---------- System Optimization Card ----------
        sys_card = tk.Frame(self.scrollable_frame, bg=BG_CARD, padx=30, pady=20)
        sys_card.pack(fill="x", padx=40, pady=(0, 20))

        tk.Label(
            sys_card, text="System Optimization", font=self.app.font_heading,
            bg=BG_CARD, fg=TEXT_WHITE
        ).pack(anchor="w", pady=(0, 20))

        # Default Unit
        tk.Label(sys_card, text="DEFAULT UNIT", font=self.app.font_body, bg=BG_CARD, fg=TEXT_LIGHT).pack(anchor="w")
        self.default_unit_entry = tk.Entry(sys_card, font=self.app.font_body, width=30)
        self.default_unit_entry.pack(anchor="w", pady=(5, 5))
        tk.Label(sys_card, text="Ex: Litres", font=self.app.font_body, bg=BG_CARD, fg=TEXT_LIGHT).pack(anchor="w", pady=(0, 15))

        # Default Export Path
        tk.Label(sys_card, text="DEFAULT EXPORT PATH", font=self.app.font_body, bg=BG_CARD, fg=TEXT_LIGHT).pack(anchor="w")
        path_frame = tk.Frame(sys_card, bg=BG_CARD)
        path_frame.pack(anchor="w", fill="x", pady=(5, 5))
        self.export_path_entry = tk.Entry(path_frame, font=self.app.font_body, width=40)
        self.export_path_entry.pack(side="left", padx=(0, 10))
        self.app.make_button(path_frame, "BROWSE", BTN_BLUE, command=self._browse_export_path, width=8).pack(side="left")
        tk.Label(sys_card, text="Ex: C:\\BulkTrust\\Reports", font=self.app.font_body, bg=BG_CARD, fg=TEXT_LIGHT).pack(anchor="w", pady=(0, 15))

        self.app.make_button(sys_card, "SAVE", BTN_GREEN, command=self._save_system_settings, width=15).pack(anchor="w")

        # ---------- Database & Security Card ----------
        sec_card = tk.Frame(self.scrollable_frame, bg=BG_CARD, padx=30, pady=20)
        sec_card.pack(fill="x", padx=40, pady=(0, 40))

        tk.Label(
            sec_card, text="Database & Security", font=self.app.font_heading,
            bg=BG_CARD, fg=TEXT_WHITE
        ).pack(anchor="w", pady=(0, 20))

        # MANUAL BACKUP + BACKUP NOW
        backup_frame = tk.Frame(sec_card, bg=BG_CARD)
        backup_frame.pack(anchor="w", fill="x", pady=(0, 15))
        tk.Label(backup_frame, text="MANUAL BACKUP", font=self.app.font_body, bg=BG_CARD, fg=TEXT_LIGHT).pack(side="left", padx=(0, 20))
        self.app.make_button(backup_frame, "BACKUP NOW", BTN_BLUE, command=self._manual_backup, width=12).pack(side="left")

        # RESET DATA
        reset_frame = tk.Frame(sec_card, bg=BG_CARD)
        reset_frame.pack(anchor="w", fill="x")
        tk.Label(reset_frame, text="RESET DATA", font=self.app.font_body, bg=BG_CARD, fg=TEXT_LIGHT).pack(side="left", padx=(0, 20))
        self.app.make_button(reset_frame, "RESET DATA", BTN_RED, command=self._reset_data, width=12).pack(side="left")

    # ----------------------------------------------------------------------
    # Helper methods to read/write extra system settings (default_unit)
    # ----------------------------------------------------------------------
    def _get_system_settings_file(self):
        return os.path.join(db.path, "system_settings.csv")

    def _read_system_settings(self):
        settings_file = self._get_system_settings_file()
        if not os.path.exists(settings_file):
            return {}
        with open(settings_file, "r") as f:
            lines = f.read().strip().splitlines()
        result = {}
        for line in lines:
            if ',' in line:
                k, v = line.split(',', 1)
                result[k] = v
        return result

    def _write_system_settings(self, key, value):
        settings_file = self._get_system_settings_file()
        data = self._read_system_settings()
        data[key] = value
        with open(settings_file, "w") as f:
            for k, v in data.items():
                f.write(f"{k},{v}\n")

    # ----------------------------------------------------------------------
    # Load all settings from backend & system file
    # ----------------------------------------------------------------------
    def _load_all_settings(self):
        settings = db.get_record("settings.csv", "1")
        if settings:
            self.biz_name_entry.delete(0, tk.END)
            self.biz_name_entry.insert(0, settings.get("biz_name", ""))
            self.delivery_note_text.delete("1.0", tk.END)
            self.delivery_note_text.insert("1.0", settings.get("terms", ""))
            self.export_path_entry.delete(0, tk.END)
            self.export_path_entry.insert(0, settings.get("export_path", ""))
        else:
            self.biz_name_entry.insert(0, "untitled")
            self.delivery_note_text.insert("1.0", "no terms")
            self.export_path_entry.insert(0, "export_folder")

        sys_data = self._read_system_settings()
        self.default_unit_entry.delete(0, tk.END)
        self.default_unit_entry.insert(0, sys_data.get("default_unit", "Litres"))

    # ----------------------------------------------------------------------
    # Save handlers
    # ----------------------------------------------------------------------
    def _save_pdf_settings(self):
        biz_name = self.biz_name_entry.get().strip()
        delivery_note = self.delivery_note_text.get("1.0", tk.END).strip()
        if not biz_name:
            biz_name = "untitled"
        if not delivery_note:
            delivery_note = "no terms"

        current = db.get_record("settings.csv", "1")
        if not current:
            current = {"backup_path": "backup_folder", "export_path": "export_folder"}

        new_record = f"1,{biz_name},{delivery_note},{current.get('backup_path','backup_folder')},{current.get('export_path','export_folder')}"
        db.update_record("settings.csv", "1", new_record)
        messagebox.showinfo("Success", "PDF settings saved successfully!")

    def _save_system_settings(self):
        default_unit = self.default_unit_entry.get().strip()
        export_path = self.export_path_entry.get().strip()

        if not default_unit:
            default_unit = "Litres"
        if not export_path:
            export_path = "export_folder"

        self._write_system_settings("default_unit", default_unit)

        current = db.get_record("settings.csv", "1")
        if not current:
            current = {"biz_name": "untitled", "terms": "no terms", "backup_path": "backup_folder"}
        new_record = f"1,{current.get('biz_name','untitled')},{current.get('terms','no terms')},{current.get('backup_path','backup_folder')},{export_path}"
        db.update_record("settings.csv", "1", new_record)

        messagebox.showinfo("Success", "System settings saved successfully!")

    def _browse_export_path(self):
        folder = filedialog.askdirectory(title="Select Default Export Folder")
        if folder:
            self.export_path_entry.delete(0, tk.END)
            self.export_path_entry.insert(0, folder)

    # ----------------------------------------------------------------------
    # Database & Security actions
    # ----------------------------------------------------------------------
    def _manual_backup(self):
        try:
            db.back_up_database(True)
            messagebox.showinfo("Backup", "Database backup completed successfully!")
        except Exception as e:
            messagebox.showerror("Backup Error", f"Failed to backup: {str(e)}")

    def _reset_data(self):
        if messagebox.askyesno("Reset Data", "WARNING: This will delete ALL organizations, members, stocks, and contributions.\nThis action cannot be undone!\n\nAre you absolutely sure?"):
            try:
                db.reset_database()
                sys_file = self._get_system_settings_file()
                if os.path.exists(sys_file):
                    os.remove(sys_file)
                self._load_all_settings()
                messagebox.showinfo("Reset Complete", "Database has been reset to initial state.")
            except Exception as e:
                messagebox.showerror("Reset Error", f"Failed to reset database: {str(e)}")