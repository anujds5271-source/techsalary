"""Generate realistic salary data"""
import sys
sys.path.append('.')

import random
from sqlalchemy.orm import Session
from src.database.database import SessionLocal
from src.models.company import Company
from src.models.location import Location
from src.models.role import Role
from src.models.salary import Salary
from src.scrapers.utils import DataGenerator

class SalaryDataGenerator:
    """Generate and save salary data"""
    
    def __init__(self):
        self.db = SessionLocal()
        self.gen = DataGenerator()
    
    def add_companies(self):
        """Add companies to database"""
        print("📊 Adding companies...")
        added = 0
        
        for company_name in self.gen.COMPANIES:
            existing = self.db.query(Company).filter(
                Company.name == company_name
            ).first()
            
            if not existing:
                company = Company(
                    name=company_name,
                    industry="Technology",
                    size="5000+",
                    headquarters="India",
                    website=f"www.{company_name.lower().replace(' ', '')}.com"
                )
                self.db.add(company)
                added += 1
        
        self.db.commit()
        print(f"✅ Added {added} companies")
    
    def add_locations(self):
        """Add locations to database"""
        print("📍 Adding locations...")
        added = 0
        
        for city in self.gen.CITIES:
            existing = self.db.query(Location).filter(
                Location.city == city
            ).first()
            
            if not existing:
                location = Location(
                    city=city,
                    state="India",
                    country="India",
                    cost_of_living_index=random.uniform(50, 70)
                )
                self.db.add(location)
                added += 1
        
        self.db.commit()
        print(f"✅ Added {added} locations")
    
    def add_roles(self):
        """Add roles to database"""
        print("💼 Adding roles...")
        added = 0
        
        for role_title in self.gen.ROLES:
            existing = self.db.query(Role).filter(
                Role.title == role_title
            ).first()
            
            if not existing:
                # Determine level
                if "Senior" in role_title or "Lead" in role_title:
                    level = "Senior"
                else:
                    level = "Mid"
                
                role = Role(
                    title=role_title,
                    category="Engineering",
                    level=level
                )
                self.db.add(role)
                added += 1
        
        self.db.commit()
        print(f"✅ Added {added} roles")
    
    def generate_salaries(self, count=50):
        """Generate salary entries"""
        print(f"💰 Generating {count} salary entries...")
        
        companies = self.db.query(Company).all()
        locations = self.db.query(Location).all()
        roles = self.db.query(Role).all()
        
        if not companies or not locations or not roles:
            print("❌ Please add companies, locations, and roles first!")
            return
        
        added = 0
        
        for i in range(count):
            company = random.choice(companies)
            location = random.choice(locations)
            role = random.choice(roles)
            
            base_salary = self.gen.random_salary(role.level)
            bonus = int(base_salary * random.uniform(0.10, 0.20))
            stock = int(base_salary * random.uniform(0.15, 0.30))
            total = base_salary + bonus + stock
            
            experience = self.gen.random_experience(role.level)
            
            salary = Salary(
                company_id=company.id,
                location_id=location.id,
                role_id=role.id,
                base_salary=base_salary,
                bonus=bonus,
                stock_options=stock,
                total_compensation=total,
                years_of_experience=experience,
                years_at_company=random.randint(0, min(experience, 5)),
                employment_type="Full-time",
                is_remote=random.choice([True, False, False, False]),
                currency="INR",
                source="data_generation"
            )
            
            self.db.add(salary)
            added += 1
            
            if added % 10 == 0:
                print(f"  ✓ Generated {added} entries...")
                self.db.commit()
        
        self.db.commit()
        print(f"✅ Added {added} salary entries")
    
    def run(self, salary_count=50):
        """Run complete data generation"""
        print("=" * 60)
        print("🚀 GENERATING SALARY DATA FOR TECHSALARY")
        print("=" * 60)
        
        self.add_companies()
        self.add_locations()
        self.add_roles()
        self.generate_salaries(salary_count)
        
        # Show stats
        total_companies = self.db.query(Company).count()
        total_locations = self.db.query(Location).count()
        total_roles = self.db.query(Role).count()
        total_salaries = self.db.query(Salary).count()
        
        print("\n" + "=" * 60)
        print("📊 DATABASE STATISTICS")
        print("=" * 60)
        print(f"Companies:  {total_companies}")
        print(f"Locations:  {total_locations}")
        print(f"Roles:      {total_roles}")
        print(f"Salaries:   {total_salaries}")
        print("=" * 60)
    
    def close(self):
        """Close database connection"""
        self.db.close()

if __name__ == "__main__":
    generator = SalaryDataGenerator()
    generator.run(salary_count=100)
    generator.close()
    print("\n✅ Data generation complete!")
