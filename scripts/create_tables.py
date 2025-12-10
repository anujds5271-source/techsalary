import sys
sys.path.append('.')

from src.database.database import engine, Base
from src.models.company import Company
from src.models.location import Location
from src.models.role import Role
from src.models.salary import Salary

def create_tables():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created successfully!")

if __name__ == "__main__":
    create_tables()