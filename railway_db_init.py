import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

print("=" * 50)
print("Railway Database Initialization")
print("=" * 50)

# Get DATABASE_URL from Railway environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ ERROR: DATABASE_URL not found in environment!")
    sys.exit(1)

print(f"✅ Found DATABASE_URL")
print(f"Connecting to database...")

try:
    # Create engine
    engine = create_engine(DATABASE_URL)
    
    # Import all models
    from src.database.database import Base
    from src.models.company import Company
    from src.models.location import Location
    from src.models.role import Role
    from src.models.salary import Salary
    
    print("✅ Models imported successfully")
    
    # Create all tables
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created successfully!")
    
    # Create session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Check if data already exists
    existing_companies = session.query(Company).count()
    if existing_companies > 0:
        print(f"⚠️  Data already exists ({existing_companies} companies found)")
        print("Skipping sample data insertion")
        sys.exit(0)
    
    print("Inserting sample data...")
    
    # Add Companies
    companies_data = [
        Company(name="Google India", industry="Technology", size="10000+", headquarters="Bangalore", website="google.co.in"),
        Company(name="Amazon India", industry="E-commerce", size="50000+", headquarters="Bangalore", website="amazon.in"),
        Company(name="Microsoft India", industry="Technology", size="5000+", headquarters="Hyderabad", website="microsoft.com"),
        Company(name="Flipkart", industry="E-commerce", size="10000+", headquarters="Bangalore", website="flipkart.com"),
        Company(name="Swiggy", industry="Food Tech", size="5000+", headquarters="Bangalore", website="swiggy.com"),
    ]
    session.add_all(companies_data)
    session.commit()
    print(f"✅ Added {len(companies_data)} companies")
    
    # Add Locations
    locations_data = [
        Location(city="Bangalore", state="Karnataka", country="India", cost_of_living_index=65.5),
        Location(city="Hyderabad", state="Telangana", country="India", cost_of_living_index=55.2),
        Location(city="Mumbai", state="Maharashtra", country="India", cost_of_living_index=72.8),
        Location(city="Pune", state="Maharashtra", country="India", cost_of_living_index=58.4),
        Location(city="Delhi", state="Delhi", country="India", cost_of_living_index=60.1),
    ]
    session.add_all(locations_data)
    session.commit()
    print(f"✅ Added {len(locations_data)} locations")
    
    # Add Roles
    roles_data = [
        Role(title="Software Engineer", category="Engineering", level="Entry"),
        Role(title="Senior Software Engineer", category="Engineering", level="Mid"),
        Role(title="SDE-2", category="Engineering", level="Mid"),
        Role(title="SDE-3", category="Engineering", level="Senior"),
        Role(title="Product Manager", category="Product", level="Mid"),
        Role(title="Data Scientist", category="Data", level="Mid"),
    ]
    session.add_all(roles_data)
    session.commit()
    print(f"✅ Added {len(roles_data)} roles")
    
    # Add Sample Salaries
    salaries_data = [
        Salary(company_id=1, role_id=2, location_id=1, base_salary=2500000, bonus=300000, stock_options=500000, total_compensation=3300000, years_of_experience=5, employment_type="Full-time", is_remote=False, currency="INR"),
        Salary(company_id=2, role_id=3, location_id=1, base_salary=2200000, bonus=250000, stock_options=400000, total_compensation=2850000, years_of_experience=4, employment_type="Full-time", is_remote=False, currency="INR"),
        Salary(company_id=3, role_id=2, location_id=2, base_salary=2400000, bonus=280000, stock_options=450000, total_compensation=3130000, years_of_experience=5, employment_type="Full-time", is_remote=False, currency="INR"),
        Salary(company_id=4, role_id=1, location_id=1, base_salary=1200000, bonus=100000, stock_options=200000, total_compensation=1500000, years_of_experience=2, employment_type="Full-time", is_remote=False, currency="INR"),
        Salary(company_id=5, role_id=5, location_id=1, base_salary=2800000, bonus=350000, stock_options=600000, total_compensation=3750000, years_of_experience=6, employment_type="Full-time", is_remote=False, currency="INR"),
    ]
    session.add_all(salaries_data)
    session.commit()
    print(f"✅ Added {len(salaries_data)} salary entries")
    
    session.close()
    
    print("=" * 50)
    print("🎉 Database initialization complete!")
    print("=" * 50)
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
