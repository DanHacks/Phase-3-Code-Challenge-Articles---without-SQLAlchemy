from lib.seed import session, Company, Dev, Freebie

# Clear existing data 
session.query(Freebie).delete()
session.query(Company).delete()
session.query(Dev).delete()
session.commit()

# Companies
company1 = Company(name="Google", founding_year=1998)
company2 = Company(name="Microsoft", founding_year=1975)
session.add_all([company1, company2])
session.commit()

# Devs
dev1 = Dev(name="Brian")
dev2 = Dev(name="Musa")
session.add_all([dev1, dev2])
session.commit()

# Freebies
company1.give_freebie(dev1, "T-Shirt", 20)
company1.give_freebie(dev2, "Laptop", 1500)
company2.give_freebie(dev1, "Mouse", 50)

# Query and Print Data
print("\nAll Developers:")
for dev in session.query(Dev).all():
    print(f"- {dev.name}")

print("\nAll Companies:")
for company in session.query(Company).all():
    print(f"- {company.name} (Founded: {company.founding_year})")

print("\nFreebies Received:")
for freebie in session.query(Freebie).all():
    print(freebie.print_details())

# Check if Brian received a laptop
print("\nDid Brian receive a Laptop?", dev1.received_one("Laptop"))

# Transfer a Freebie
freebie = session.query(Freebie).filter_by(item_name="Mouse").first()
if dev1.give_out(dev2, freebie):
    print("\nMouse has been transferred from Brian to Musa!")

# Show Companies Where Brian Got Freebies
print("\nCompanies Brian got freebies from:")
for company in dev1.companies_with_freebies:
    print(f"- {company.name}")

session.close()
