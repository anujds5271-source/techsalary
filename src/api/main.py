from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.models.company import Company
from src.models.location import Location
from src.models.role import Role
from src.models.salary import Salary

# Create FastAPI app
app = FastAPI(
    title="TechSalary.in API",
    description="India's Salary Data Platform",
    version="0.1.0"
)

# Mount static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# ============================================
# HTML PAGES (Frontend)
# ============================================

@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    """Homepage with search form"""
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/submit", response_class=HTMLResponse)
async def submit_page(request: Request):
    """Salary submission page"""
    return templates.TemplateResponse("submit.html", {"request": request})

# ============================================
# API ENDPOINTS (Backend)
# ============================================

@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected"
    }

@app.get("/api/companies")
def get_companies(db: Session = Depends(get_db)):
    """Get all companies"""
    companies = db.query(Company).all()
    return {
        "total": len(companies),
        "data": [
            {
                "id": c.id,
                "name": c.name,
                "industry": c.industry,
                "size": c.size,
                "headquarters": c.headquarters
            } for c in companies
        ]
    }

@app.get("/api/locations")
def get_locations(db: Session = Depends(get_db)):
    """Get all locations"""
    locations = db.query(Location).all()
    return {
        "total": len(locations),
        "data": [
            {
                "id": l.id,
                "city": l.city,
                "state": l.state,
                "cost_of_living_index": l.cost_of_living_index
            } for l in locations
        ]
    }

@app.get("/api/roles")
def get_roles(db: Session = Depends(get_db)):
    """Get all roles"""
    roles = db.query(Role).all()
    return {
        "total": len(roles),
        "data": [
            {
                "id": r.id,
                "title": r.title,
                "category": r.category,
                "level": r.level
            } for r in roles
        ]
    }

@app.get("/api/salaries")
def get_salaries(db: Session = Depends(get_db)):
    """Get all salaries"""
    salaries = db.query(Salary).all()
    
    results = []
    for s in salaries:
        company = db.query(Company).filter(Company.id == s.company_id).first()
        role = db.query(Role).filter(Role.id == s.role_id).first()
        location = db.query(Location).filter(Location.id == s.location_id).first()
        
        results.append({
            "id": s.id,
            "company": company.name,
            "role": role.title,
            "location": f"{location.city}",
            "total_compensation": s.total_compensation,
            "base_salary": s.base_salary,
            "bonus": s.bonus,
            "stock_options": s.stock_options,
            "years_of_experience": s.years_of_experience,
            "employment_type": s.employment_type,
            "currency": s.currency
        })
    
    return {
        "total": len(results),
        "data": results
    }

@app.get("/api/salaries/{salary_id}")
def get_salary_by_id(salary_id: int, db: Session = Depends(get_db)):
    """Get single salary by ID"""
    salary = db.query(Salary).filter(Salary.id == salary_id).first()
    if not salary:
        return {"error": "Salary not found"}
    
    company = db.query(Company).filter(Company.id == salary.company_id).first()
    role = db.query(Role).filter(Role.id == salary.role_id).first()
    location = db.query(Location).filter(Location.id == salary.location_id).first()
    
    return {
        "id": salary.id,
        "company": {
            "name": company.name,
            "industry": company.industry,
            "size": company.size
        },
        "role": {
            "title": role.title,
            "category": role.category,
            "level": role.level
        },
        "location": {
            "city": location.city,
            "state": location.state
        },
        "compensation": {
            "total": salary.total_compensation,
            "base": salary.base_salary,
            "bonus": salary.bonus,
            "stocks": salary.stock_options,
            "currency": salary.currency
        },
        "experience": {
            "years_total": salary.years_of_experience,
            "years_at_company": salary.years_at_company
        },
        "details": {
            "employment_type": salary.employment_type,
            "is_remote": salary.is_remote,
            "submission_date": salary.submission_date.isoformat() if salary.submission_date else None
        }
    }

# ============================================
# INCLUDE ADVANCED ROUTES
# ============================================

from src.api.routes import router
app.include_router(router)