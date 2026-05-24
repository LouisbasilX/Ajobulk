import backend_logic as db

def seed_members():
    members_data = [
        ("Adebayo Ogunlesi", "08012345678"),
        ("Chioma Nwosu", "08023456789"),
        ("Emeka Okonkwo", "08034567890"),
        ("Funmilayo Ransome-Kuti", "08045678901"),
        ("Gbenga Adeyinka", "08056789012"),
        ("Hadiza Bello", "08067890123"),
        ("Ikenna Obi", "08078901234"),
        ("Joy Okafor", "08089012345"),
        ("Kunle Ajayi", "08090123456"),
        ("Lola Shoneyin", "08101234567"),
        ("Musa Danladi", "08112345678"),
        ("Ngozi Okonjo", "08123456789"),
        ("Olu Jacobs", "08134567890"),
        ("Patience Jonathan", "08145678901"),
        ("Quadri Olanrewaju", "08156789012"),
        ("Ruth Kadiri", "08167890123"),
        ("Sade Adu", "08178901234"),
        ("Tunde Kelani", "08189012345"),
        ("Uche Jombo", "08190123456"),
        ("Victoria Ogunleye", "08201234567")
    ]
    
    print("🌱 Seeding 20 members...")
    for name, phone in members_data:
        result = db.create_member(name, phone)
        print(f"  ➕ {name}: {result}")

if __name__ == "__main__":
    seed_members()