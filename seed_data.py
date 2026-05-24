# seed_data.py
import backend_logic as db

def seed_organizations():
    """Add 5 sample organizations with Nigerian market names."""
    org_names = [
        "Carawomen Cooperative",
        "Ajo Women Thrift",
        "Alaba Market Traders",
        "Ounje Aje Food Sellers",
        "Ibadan Ajo Group"
    ]
    
    print("🌱 Seeding organizations...")
    for name in org_names:
        result = db.add_organization(name)
        print(f"  ➕ {name}: {result}")

if __name__ == "__main__":
    seed_organizations()