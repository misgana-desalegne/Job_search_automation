import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional
import re

class ContactFinder:
    """Find company contact information"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def find_company_info(self, company_name: str, company_website: Optional[str] = None) -> Dict:
        """
        Find company contact information
        
        Args:
            company_name: Company name
            company_website: Company website URL (optional)
        
        Returns:
            Dictionary with contact information
        """
        info = {
            'company_name': company_name,
            'email': None,
            'phone': None,
            'website': company_website,
            'social_media': {}
        }
        
        if company_website:
            try:
                info.update(self._scrape_company_website(company_website))
            except Exception as e:
                print(f"Error scraping website: {e}")
        
        return info
    
    def _scrape_company_website(self, website_url: str) -> Dict:
        """Scrape company website for contact info"""
        try:
            response = requests.get(website_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract emails
            emails = self._extract_emails(soup.get_text())
            
            # Extract phone numbers
            phones = self._extract_phone_numbers(soup.get_text())
            
            # Look for Contact page
            contact_page = self._find_contact_page(soup, website_url)
            
            return {
                'email': emails[0] if emails else None,
                'phone': phones[0] if phones else None,
                'has_contact_page': bool(contact_page),
                'contact_page_url': contact_page
            }
        
        except Exception as e:
            print(f"Error in _scrape_company_website: {e}")
            return {}
    
    @staticmethod
    def _extract_emails(text: str) -> list:
        """Extract email addresses from text"""
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = re.findall(email_pattern, text)
        # Filter out common non-contact emails
        filtered = [e for e in emails if not any(x in e.lower() for x in ['noreply', 'notification', 'bot'])]
        return list(set(filtered))[:5]  # Return unique, limit to 5
    
    @staticmethod
    def _extract_phone_numbers(text: str) -> list:
        """Extract phone numbers from text"""
        phone_pattern = r'\+?33[0-9]{9}|\+?33\s?[0-9]{9}|0[0-9]{9}'
        phones = re.findall(phone_pattern, text)
        return list(set(phones))[:3]
    
    @staticmethod
    def _find_contact_page(soup: BeautifulSoup, base_url: str) -> Optional[str]:
        """Find contact page URL"""
        for link in soup.find_all('a'):
            href = link.get('href', '')
            text = link.get_text(strip=True).lower()
            
            if 'contact' in text or 'contact' in href.lower():
                if href.startswith('http'):
                    return href
                elif href.startswith('/'):
                    return base_url.rstrip('/') + href
        
        return None
    
    def enrich_job_posting(self, job_data: Dict) -> Dict:
        """
        Enrich job posting with company contact information
        
        Args:
            job_data: Job posting data
        
        Returns:
            Enhanced job data with contact information
        """
        try:
            company_info = self.find_company_info(
                job_data.get('company_name'),
                job_data.get('company_website')
            )
            
            job_data['company_contact_email'] = company_info.get('email')
            job_data['company_contact_phone'] = company_info.get('phone')
            job_data['company_website'] = company_info.get('website')
            
            return job_data
        
        except Exception as e:
            print(f"Error enriching job posting: {e}")
            return job_data
