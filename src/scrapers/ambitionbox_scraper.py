import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from .utils import ScraperUtils

class AmbitionBoxScraper:
    """Scraper for AmbitionBox salary data"""
    
    BASE_URL = "https://www.ambitionbox.com"
    
    def __init__(self):
        self.utils = ScraperUtils()
        self.session = requests.Session()
        self.session.headers.update(self.utils.get_headers())
    
    def get_company_salaries(self, company_slug: str) -> List[Dict]:
        """
        Scrape salaries for a specific company
        Example: company_slug = "google-salaries"
        """
        url = f"{self.BASE_URL}/salaries/{company_slug}"
        
        try:
            print(f"Scraping: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'lxml')
            salaries = []
            
            # Find salary cards (adjust selectors based on actual HTML)
            salary_cards = soup.select('.salary-card')  # Example selector
            
            for card in salary_cards:
                salary_data = self._parse_salary_card(card)
                if salary_data:
                    salaries.append(salary_data)
            
            print(f"✅ Found {len(salaries)} salary entries")
            self.utils.random_delay()
            
            return salaries
            
        except Exception as e:
            print(f"❌ Error scraping {company_slug}: {e}")
            return []
    
    def _parse_salary_card(self, card) -> Dict:
        """Parse individual salary card"""
        try:
            # Extract data (adjust selectors)
            role = self.utils.safe_find(card, '.role-title')
            salary_text = self.utils.safe_find(card, '.salary-amount')
            experience = self.utils.safe_find(card, '.experience')
            location = self.utils.safe_find(card, '.location')
            
            # Parse salary
            salary = self.utils.parse_salary(salary_text)
            
            return {
                'role': role,
                'salary': salary * 100000,  # Convert lakhs to rupees
                'experience': experience,
                'location': location,
                'source': 'AmbitionBox'
            }
            
        except Exception as e:
            print(f"Error parsing card: {e}")
            return None
    
    def scrape_top_companies(self, companies: List[str]) -> List[Dict]:
        """Scrape multiple companies"""
        all_salaries = []
        
        for company in companies:
            print(f"\n🔍 Scraping {company}...")
            salaries = self.get_company_salaries(f"{company.lower()}-salaries")
            all_salaries.extend(salaries)
            self.utils.random_delay(3, 6)  # Longer delay between companies
        
        return all_salaries

# Usage example:
if __name__ == "__main__":
    scraper = AmbitionBoxScraper()
    
    companies = ['google', 'amazon', 'microsoft', 'flipkart']
    data = scraper.scrape_top_companies(companies)
    
    print(f"\n✅ Total scraped: {len(data)} entries")

## **⚠️ IMPORTANT: WEB SCRAPING ETHICS & LEGALITY**

### **Before Scraping:**

#1. **Check robots.txt:**
https://www.ambitionbox.com/robots.txt
https://www.glassdoor.co.in/robots.txt