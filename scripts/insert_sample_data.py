import sys
sys.path.append('.')

from src.database.database import SessionLocal
from src.models.company import Company
from src.models.location import Location
from src.models.role import Role
from src.models.salary import Salary

def insert_sample_data():
    db = SessionLocal()
    
    try:
        print("Inserting sample data...")
        
        # 1. Companies
        companies = [
            Company(name="Google India", industry="Technology", size="Large", headquarters="Bangalore", website="google.co.in"),
            Company(name="Amazon India", industry="E-commerce", size="Large", headquarters="Bangalore", website="amazon.in"),
            Company(name="Microsoft India", industry="Technology", size="Large", headquarters="Hyderabad", website="microsoft.com/en-in"),
            Company(name="Flipkart", industry="E-commerce", size="Large", headquarters="Bangalore", website="flipkart.com"),
            Company(name="Swiggy", industry="Food Tech", size="Mid-size", headquarters="Bangalore", website="swiggy.com"),
        ]
        db.add_all(companies)
        db.commit()
        print("✅ Companies added!")
        
        # 2. Locations
        locations = [
            Location(city="Bangalore", state="Karnataka", cost_of_living_index=85.5),
            Location(city="Hyderabad", state="Telangana", cost_of_living_index=72.3),
            Location(city="Mumbai", state="Maharashtra", cost_of_living_index=95.8),
            Location(city="Pune", state="Maharashtra", cost_of_living_index=78.4),
            Location(city="Delhi", state="Delhi", cost_of_living_index=88.2),
        ]
        db.add_all(locations)
        db.commit()
        print("✅ Locations added!")
        
        # 3. Roles
        roles = [
            Role(title="Software Engineer", category="Engineering", level="Mid"),
            Role(title="Senior Software Engineer", category="Engineering", level="Senior"),
            Role(title="SDE-2", category="Engineering", level="Mid"),
            Role(title="SDE-3", category="Engineering", level="Senior"),
            Role(title="Product Manager", category="Product", level="Mid"),
            Role(title="Data Scientist", category="Data", level="Mid"),
        ]
        db.add_all(roles)
        db.commit()
        print("✅ Roles added!")
        
        # 4. Salaries
        salaries = [
            Salary(
                company_id=1, role_id=1, location_id=1,
                base_salary=2000000, bonus=300000, stock_options=200000,
                total_compensation=2500000, years_of_experience=3,
                years_at_company=2, employment_type="Full-time",
                is_remote=False, source="user_submission"
            ),
            Salary(
                company_id=2, role_id=3, location_id=2,
                base_salary=2800000, bonus=400000, stock_options=0,
                total_compensation=3200000, years_of_experience=5,
                years_at_company=3, employment_type="Full-time",
                is_remote=False, source="user_submission"
            ),
            Salary(
                company_id=3, role_id=2, location_id=2,
                base_salary=3000000, bonus=500000, stock_options=300000,
                total_compensation=3800000, years_of_experience=6,
                years_at_company=4, employment_type="Full-time",
                is_remote=False, source="user_submission"
            ),
            Salary(
                company_id=4, role_id=1, location_id=1,
                base_salary=1800000, bonus=200000, stock_options=100000,
                total_compensation=2100000, years_of_experience=2,
                years_at_company=1, employment_type="Full-time",
                is_remote=False, source="user_submission"
            ),
            Salary(
                company_id=5, role_id=5, location_id=1,
                base_salary=2200000, bonus=300000, stock_options=0,
                total_compensation=2500000, years_of_experience=4,
                years_at_company=2, employment_type="Full-time",
                is_remote=False, source="user_submission"
            ),
        ]
        db.add_all(salaries)
        db.commit()
        print("✅ Salaries added!")
        
        print("\n🎉 All sample data inserted successfully!")
        print(f"📊 Total entries:")
        print(f"   - Companies: {len(companies)}")
        print(f"   - Locations: {len(locations)}")
        print(f"   - Roles: {len(roles)}")
        print(f"   - Salaries: {len(salaries)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    insert_sample_data()