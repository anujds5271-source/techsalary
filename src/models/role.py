from sqlalchemy import Column, Integer, String
from src.database.database import Base

class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), unique=True, nullable=False, index=True)
    category = Column(String(100))
    level = Column(String(50))
    
    def __repr__(self):
        return f"<Role {self.title}>"