# settings_manager.py
import json
import os

SETTINGS_FILE = "app_settings.json"

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {"quick_links": []}
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)

def add_quick_link(stock_id, stock_name, org_name):
    settings = load_settings()
    links = settings.get("quick_links", [])
    # Remove if already present
    links = [l for l in links if l["stock_id"] != stock_id]
    # Insert at front
    links.insert(0, {"stock_id": stock_id, "stock_name": stock_name, "org_name": org_name})
    # Keep only last 3
    settings["quick_links"] = links[:3]
    save_settings(settings)

def get_quick_links():
    return load_settings().get("quick_links", [])