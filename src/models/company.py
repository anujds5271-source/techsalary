from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from src.database.database import Base

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), unique=True, nullable=False, index=True)
    industry = Column(String(100))
    size = Column(String(50))
    headquarters = Column(String(100))
    website = Column(String(200))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Company {self.name}>"