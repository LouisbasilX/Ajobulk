import tkinter as tk
from base_window import AjobulkApp
from dashboard_frame import DashboardFrame
from members_frame import MembersFrame
from settings_frame import SettingsFrame
def main():
    app = AjobulkApp()

    # load dashboard as the first screen
    app.show_frame(DashboardFrame)

    # wire sidebar nav buttons to screens
    app.bind("<<Nav-dashboard>>", lambda e: app.show_frame(DashboardFrame))
    app.bind("<<Nav-members>>",   lambda e: app.show_frame(MembersFrame))
    app.bind("<<Nav-settings>>",  lambda e: app.show_frame(SettingsFrame))

    app.mainloop()

if __name__ == "__main__":
    main()