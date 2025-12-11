import sys
sys.path.append('.')
import random
from src.database.database import SessionLocal
from src.models.company import Company
from src.models.location import Location
from src.models.role import Role
from src.models.salary import Salary

print("🔄 Adding CORRECT Indian salary data...")

db = SessionLocal()

# Delete old data
db.query(Salary).delete()
db.commit()
print("✅ Cleared old data")

# CORRECT salary ranges by company
CORRECT_RANGES = {
    # Service companies (Lower salaries)
    "TCS": {"Entry": (320000, 450000), "Mid": (650000, 1200000), "Senior": (1200000, 2200000)},
    "Infosys": {"Entry": (380000, 500000), "Mid": (700000, 1300000), "Senior": (1300000, 2400000)},
    "Wipro": {"Entry": (350000, 480000), "Mid": (680000, 1250000), "Senior": (1250000, 2300000)},
    "HCL Technologies": {"Entry": (340000, 470000), "Mid": (670000, 1230000), "Senior": (1230000, 2250000)},
    "Tech Mahindra": {"Entry": (360000, 490000), "Mid": (690000, 1270000), "Senior": (1270000, 2350000)},
    "Capgemini": {"Entry": (400000, 550000), "Mid": (750000, 1350000), "Senior": (1350000, 2500000)},
    "Cognizant": {"Entry": (380000, 520000), "Mid": (720000, 1320000), "Senior": (1320000, 2450000)},
    "Accenture India": {"Entry": (450000, 600000), "Mid": (800000, 1450000), "Senior": (1450000, 2700000)},
    
    # Mid-tier (Medium salaries)
    "Flipkart": {"Entry": (900000, 1500000), "Mid": (1500000, 2800000), "Senior": (2800000, 5500000)},
    "Swiggy": {"Entry": (1000000, 1600000), "Mid": (1600000, 3000000), "Senior": (3000000, 6000000)},
    "Zomato": {"Entry": (950000, 1550000), "Mid": (1550000, 2900000), "Senior": (2900000, 5800000)},
    "PhonePe": {"Entry": (1100000, 1700000), "Mid": (1700000, 3200000), "Senior": (3200000, 6500000)},
    "Razorpay": {"Entry": (1000000, 1650000), "Mid": (1650000, 3100000), "Senior": (3100000, 6200000)},
    "CRED": {"Entry": (1200000, 1800000), "Mid": (1800000, 3500000), "Senior": (3500000, 7000000)},
    "Paytm": {"Entry": (800000, 1350000), "Mid": (1350000, 2500000), "Senior": (2500000, 5000000)},
    "Ola": {"Entry": (850000, 1400000), "Mid": (1400000, 2600000), "Senior": (2600000, 5200000)},
    
    # Top-tier (High salaries)
    "Google India": {"Entry": (1500000, 2500000), "Mid": (2500000, 5000000), "Senior": (5000000, 12000000)},
    "Amazon India": {"Entry": (1400000, 2200000), "Mid": (2200000, 4500000), "Senior": (4500000, 10000000)},
    "Microsoft India": {"Entry": (1500000, 2400000), "Mid": (2400000, 4800000), "Senior": (4800000, 11000000)},
}

companies = db.query(Company).all()
locations = db.query(Location).all()
roles = db.query(Role).all()

added = 0
exp_ranges = {"Entry": (0, 2), "Mid": (3, 7), "Senior": (8, 15)}

# Generate 300 entries
for i in range(300):
    company = random.choice(companies)
    location = random.choice(locations)
    role = random.choice(roles)
    
    # Get correct range for this company
    if company.name in CORRECT_RANGES:
        salary_range = CORRECT_RANGES[company.name][role.level]
    else:
        # Default for unknown companies
        salary_range = {"Entry": (400000, 800000), "Mid": (900000, 1800000), "Senior": (2000000, 4000000)}[role.level]
    
    base = random.randint(*salary_range)
    
    # Calculate bonus and stock based on company tier
    if company.name in ["Google India", "Amazon India", "Microsoft India"]:
        bonus = int(base * random.uniform(0.15, 0.25))
        stock = int(base * random.uniform(0.30, 0.50))
    elif company.name in ["Flipkart", "Swiggy", "Razorpay", "PhonePe", "CRED"]:
        bonus = int(base * random.uniform(0.10, 0.20))
        stock = int(base * random.uniform(0.20, 0.35))
    else:  # Service companies
        bonus = int(base * random.uniform(0.05, 0.12))
        stock = int(base * random.uniform(0.00, 0.05))
    
    total = base + bonus + stock
    exp = random.randint(*exp_ranges[role.level])
    
    salary = Salary(
        company_id=company.id,
        location_id=location.id,
        role_id=role.id,
        base_salary=base,
        bonus=bonus,
        stock_options=stock,
        total_compensation=total,
        years_of_experience=exp,
        employment_type="Full-time",
        currency="INR",
        source="correct_indian_market_2024"
    )
    
    db.add(salary)
    added += 1
    
    if added % 100 == 0:
        db.commit()
        print(f"✓ Added {added} entries...")

db.commit()
db.close()

print(f"\n✅ Added {added} CORRECT salary entries!")
print("Average salary should now be 12-18L (realistic!)")
