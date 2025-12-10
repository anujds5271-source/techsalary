from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class SalaryBase(BaseModel):
    company_id: int
    role_id: int
    location_id: int
    base_salary: float = Field(gt=0)
    bonus: float = Field(default=0, ge=0)
    stock_options: float = Field(default=0, ge=0)
    total_compensation: float = Field(gt=0)
    years_of_experience: int = Field(ge=0)
    years_at_company: Optional[int] = Field(default=None, ge=0)
    employment_type: str = "Full-time"
    is_remote: bool = False
    currency: str = "INR"
    source: str = "user_submission"

class SalaryCreate(SalaryBase):
    pass

class SalaryResponse(BaseModel):
    id: int
    company_name: str
    role_title: str
    location_city: str
    location_state: str
    base_salary: float
    bonus: float
    stock_options: float
    total_compensation: float
    years_of_experience: int
    employment_type: str
    currency: str
    
    class Config:
        from_attributes = True

class SalaryDetailResponse(SalaryResponse):
    company_industry: str
    company_size: str
    role_category: str
    role_level: str
    years_at_company: Optional[int]
    is_remote: bool
    submission_date: Optional[datetime]
    
    class Config:
        from_attributes = True