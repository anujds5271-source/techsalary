import sys
sys.path.append('.')
from src.database.database import SessionLocal
from src.models.salary import Salary

db = SessionLocal()
count = db.query(Salary).delete()
db.commit()
db.close()

print(f"🗑️  Deleted {count} salary entries")
print("✅ Database is now empty - ready for fresh data!")
