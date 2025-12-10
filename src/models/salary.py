from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from src.database.database import Base

class Salary(Base):
    __tablename__ = "salaries"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Keys
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False, index=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False, index=True)
    
    # Salary Details
    base_salary = Column(Float, nullable=False)
    bonus = Column(Float, default=0)
    stock_options = Column(Float, default=0)
    total_compensation = Column(Float, nullable=False)
    
    # Experience
    years_of_experience = Column(Integer, nullable=False)
    years_at_company = Column(Integer)
    
    # Additional Info
    employment_type = Column(String(50))
    is_remote = Column(Boolean, default=False)
    currency = Column(String(10), default="INR")
    
    # Metadata
    submission_date = Column(DateTime(timezone=True), server_default=func.now())
    is_verified = Column(Boolean, default=False)
    source = Column(String(100))
    
    def __repr__(self):
        return f"<Salary {self.total_compensation} INR>"