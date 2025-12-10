"""Utility functions for data generation"""
import random

class DataGenerator:
    """Generate realistic salary data"""
    
    COMPANIES = [
        "TCS", "Infosys", "Wipro", "HCL", "Tech Mahindra",
        "Accenture", "IBM India", "Oracle India", "Adobe India",
        "Cognizant", "Capgemini", "LTI", "Mindtree", "Mphasis"
    ]
    
    CITIES = [
        "Bangalore", "Hyderabad", "Pune", "Mumbai", "Delhi",
        "Gurgaon", "Noida", "Chennai", "Kolkata", "Ahmedabad"
    ]
    
    ROLES = [
        "Software Engineer", "Senior Software Engineer", "Lead Engineer",
        "DevOps Engineer", "QA Engineer", "Data Engineer",
        "Frontend Developer", "Backend Developer", "Full Stack Developer"
    ]
    
    @staticmethod
    def random_salary(level):
        """Generate random salary based on level"""
        ranges = {
            "Entry": (600000, 1500000),
            "Mid": (1500000, 3500000),
            "Senior": (3500000, 7000000)
        }
        return random.randint(*ranges[level])
    
    @staticmethod
    def random_experience(level):
        """Generate random experience"""
        ranges = {
            "Entry": (0, 2),
            "Mid": (3, 7),
            "Senior": (8, 15)
        }
        return random.randint(*ranges[level])

print("✅ Utils module created")
