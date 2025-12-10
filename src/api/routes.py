from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import Optional, List
from src.database.database import get_db
from src.models.company import Company
from src.models.location import Location
from src.models.role import Role
from src.models.salary import Salary

router = APIRouter(prefix="/api", tags=["salaries"])

@router.get("/search/salaries")
def search_salaries(
    company: Optional[str] = Query(None, description="Company name"),
    city: Optional[str] = Query(None, description="City name"),
    role: Optional[str] = Query(None, description="Role title"),
    min_salary: Optional[float] = Query(None, description="Minimum salary"),
    max_salary: Optional[float] = Query(None, description="Maximum salary"),
    min_experience: Optional[int] = Query(None, description="Minimum years of experience"),
    max_experience: Optional[int] = Query(None, description="Maximum years of experience"),
    employment_type: Optional[str] = Query(None, description="Employment type"),
    is_remote: Optional[bool] = Query(None, description="Remote jobs only"),
    limit: int = Query(10, ge=1, le=100, description="Number of results"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    db: Session = Depends(get_db)
):
    """
    🔍 Advanced Salary Search
    
    Search and filter salaries by multiple criteria:
    - Company name
    - Location (city)
    - Job role
    - Salary range
    - Experience range
    - Employment type
    - Remote/On-site
    """
    
    query = db.query(Salary).join(Company).join(Role).join(Location)
    
    # Apply filters
    filters = []
    
    if company:
        filters.append(Company.name.ilike(f"%{company}%"))
    
    if city:
        filters.append(Location.city.ilike(f"%{city}%"))
    
    if role:
        filters.append(Role.title.ilike(f"%{role}%"))
    
    if min_salary:
        filters.append(Salary.total_compensation >= min_salary)
    
    if max_salary:
        filters.append(Salary.total_compensation <= max_salary)
    
    if min_experience is not None:
        filters.append(Salary.years_of_experience >= min_experience)
    
    if max_experience is not None:
        filters.append(Salary.years_of_experience <= max_experience)
    
    if employment_type:
        filters.append(Salary.employment_type == employment_type)
    
    if is_remote is not None:
        filters.append(Salary.is_remote == is_remote)
    
    if filters:
        query = query.filter(and_(*filters))
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    salaries = query.offset(offset).limit(limit).all()
    
    # Format results
    results = []
    for s in salaries:
        company_obj = db.query(Company).filter(Company.id == s.company_id).first()
        role_obj = db.query(Role).filter(Role.id == s.role_id).first()
        location_obj = db.query(Location).filter(Location.id == s.location_id).first()
        
        results.append({
            "id": s.id,
            "company": company_obj.name,
            "role": role_obj.title,
            "location": f"{location_obj.city}, {location_obj.state}",
            "total_compensation": s.total_compensation,
            "base_salary": s.base_salary,
            "bonus": s.bonus,
            "stock_options": s.stock_options,
            "years_of_experience": s.years_of_experience,
            "employment_type": s.employment_type,
            "is_remote": s.is_remote,
            "currency": s.currency
        })
    
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "results": len(results),
        "data": results
    }


@router.get("/salaries/by-company/{company_name}")
def get_salaries_by_company(company_name: str, db: Session = Depends(get_db)):
    """Get all salaries for a specific company"""
    
    company = db.query(Company).filter(Company.name.ilike(f"%{company_name}%")).first()
    
    if not company:
        return {"error": "Company not found", "data": []}
    
    salaries = db.query(Salary).filter(Salary.company_id == company.id).all()
    
    results = []
    for s in salaries:
        role = db.query(Role).filter(Role.id == s.role_id).first()
        location = db.query(Location).filter(Location.id == s.location_id).first()
        
        results.append({
            "id": s.id,
            "role": role.title,
            "location": f"{location.city}",
            "total_compensation": s.total_compensation,
            "years_of_experience": s.years_of_experience
        })
    
    return {
        "company": company.name,
        "total_salaries": len(results),
        "data": results
    }


@router.get("/salaries/by-location/{city}")
def get_salaries_by_location(city: str, db: Session = Depends(get_db)):
    """Get all salaries for a specific city"""
    
    location = db.query(Location).filter(Location.city.ilike(f"%{city}%")).first()
    
    if not location:
        return {"error": "Location not found", "data": []}
    
    salaries = db.query(Salary).filter(Salary.location_id == location.id).all()
    
    results = []
    for s in salaries:
        company = db.query(Company).filter(Company.id == s.company_id).first()
        role = db.query(Role).filter(Role.id == s.role_id).first()
        
        results.append({
            "id": s.id,
            "company": company.name,
            "role": role.title,
            "total_compensation": s.total_compensation,
            "years_of_experience": s.years_of_experience
        })
    
    return {
        "location": f"{location.city}, {location.state}",
        "total_salaries": len(results),
        "average_salary": sum(s.total_compensation for s in salaries) / len(salaries) if salaries else 0,
        "data": results
    }


@router.get("/stats/salary-range")
def get_salary_range_stats(db: Session = Depends(get_db)):
    """Get salary statistics and ranges"""
    
    salaries = db.query(Salary).all()
    
    if not salaries:
        return {"error": "No data available"}
    
    compensations = [s.total_compensation for s in salaries]
    
    return {
        "total_entries": len(salaries),
        "min_salary": min(compensations),
        "max_salary": max(compensations),
        "average_salary": sum(compensations) / len(compensations),
        "median_salary": sorted(compensations)[len(compensations) // 2]
    }


from src.schemas.salary import SalaryCreate

@router.post("/salaries/submit")
def submit_salary(
    salary_data: SalaryCreate,
    db: Session = Depends(get_db)
):
    """
    📝 Submit New Salary Data
    
    Users can submit their salary information anonymously.
    """
    
    # Verify company exists
    company = db.query(Company).filter(Company.id == salary_data.company_id).first()
    if not company:
        return {"error": "Company not found"}
    
    # Verify role exists
    role = db.query(Role).filter(Role.id == salary_data.role_id).first()
    if not role:
        return {"error": "Role not found"}
    
    # Verify location exists
    location = db.query(Location).filter(Location.id == salary_data.location_id).first()
    if not location:
        return {"error": "Location not found"}
    
    # Create new salary entry
    new_salary = Salary(
        company_id=salary_data.company_id,
        role_id=salary_data.role_id,
        location_id=salary_data.location_id,
        base_salary=salary_data.base_salary,
        bonus=salary_data.bonus,
        stock_options=salary_data.stock_options,
        total_compensation=salary_data.total_compensation,
        years_of_experience=salary_data.years_of_experience,
        years_at_company=salary_data.years_at_company,
        employment_type=salary_data.employment_type,
        is_remote=salary_data.is_remote,
        currency=salary_data.currency,
        source=salary_data.source,
        is_verified=False
    )
    
    db.add(new_salary)
    db.commit()
    db.refresh(new_salary)
    
    return {
        "message": "Salary submitted successfully!",
        "id": new_salary.id,
        "company": company.name,
        "role": role.title,
        "location": f"{location.city}, {location.state}",
        "total_compensation": new_salary.total_compensation
    }


@router.post("/companies/add")
def add_company(
    name: str,
    industry: Optional[str] = None,
    size: Optional[str] = None,
    headquarters: Optional[str] = None,
    website: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    🏢 Add New Company
    
    Add a company if it doesn't exist in database.
    """
    
    # Check if company already exists
    existing = db.query(Company).filter(Company.name == name).first()
    if existing:
        return {"error": "Company already exists", "id": existing.id, "name": existing.name}
    
    new_company = Company(
        name=name,
        industry=industry,
        size=size,
        headquarters=headquarters,
        website=website
    )
    
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    
    return {
        "message": "Company added successfully!",
        "id": new_company.id,
        "name": new_company.name,
        "industry": new_company.industry
    }


@router.post("/locations/add")
def add_location(
    city: str,
    state: str,
    country: str = "India",
    cost_of_living_index: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """
    📍 Add New Location
    
    Add a location if it doesn't exist in database.
    """
    
    # Check if location already exists
    existing = db.query(Location).filter(
        Location.city == city,
        Location.state == state
    ).first()
    
    if existing:
        return {"error": "Location already exists", "id": existing.id}
    
    new_location = Location(
        city=city,
        state=state,
        country=country,
        cost_of_living_index=cost_of_living_index
    )
    
    db.add(new_location)
    db.commit()
    db.refresh(new_location)
    
    return {
        "message": "Location added successfully!",
        "id": new_location.id,
        "city": new_location.city,
        "state": new_location.state
    }


@router.post("/roles/add")
def add_role(
    title: str,
    category: Optional[str] = None,
    level: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    💼 Add New Role
    
    Add a job role if it doesn't exist in database.
    """
    
    # Check if role already exists
    existing = db.query(Role).filter(Role.title == title).first()
    if existing:
        return {"error": "Role already exists", "id": existing.id, "title": existing.title}
    
    new_role = Role(
        title=title,
        category=category,
        level=level
    )
    
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    
    return {
        "message": "Role added successfully!",
        "id": new_role.id,
        "title": new_role.title,
        "category": new_role.category
    }