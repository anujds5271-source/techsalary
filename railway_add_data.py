import os
os.environ['DATABASE_URL'] = os.getenv('DATABASE_URL', 'postgresql://localhost:5432/techsalary')

import sys
sys.path.append('.')

from src.scrapers.data_generator import SalaryDataGenerator

print("🚀 Running data generation on Railway...")
generator = SalaryDataGenerator()
generator.run(salary_count=100)
generator.close()
print("✅ Railway data generation complete!")
