from sqlalchemy import Column, Integer, String, Float
from src.database.database import Base

class Location(Base):
    __tablename__ = "locations"
    
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String(100), nullable=False, index=True)
    state = Column(String(100), nullable=False)
    country = Column(String(100), default="India")
    cost_of_living_index = Column(Float)
    
    def __repr__(self):
        return f"<Location {self.city}, {self.state}>"