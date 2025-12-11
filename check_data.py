import sys
sys.path.append('.')
from src.database.database import SessionLocal
from src.models.salary import Salary
from src.models.company import Company
from src.models.role import Role
from src.models.location import Location

db = SessionLocal()

# Total stats
total_salaries = db.query(Salary).count()
total_companies = db.query(Company).count()

print('=' * 70)
print('📊 CURRENT DATABASE STATUS')
print('=' * 70)
print(f'Total Salaries: {total_salaries}')
print(f'Total Companies: {total_companies}')
print()

# Show 10 sample entries
print('📋 SAMPLE ENTRIES:')
print('=' * 70)

salaries = db.query(Salary).limit(10).all()

for s in salaries:
    company = db.query(Company).filter(Company.id == s.company_id).first()
    role = db.query(Role).filter(Role.id == s.role_id).first()
    location = db.query(Location).filter(Location.id == s.location_id).first()
    
    print(f'{company.name:25} | {role.title:30} | {role.level:8} | {s.years_of_experience} yrs | ₹{s.total_compensation/100000:5.1f}L')

db.close()
