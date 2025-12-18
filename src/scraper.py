import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import List, Dict
import time
import re
from config.config import config
from urllib.parse import urljoin

class IndeedScraper:
    """Scraper for Indeed job postings"""
    
    def __init__(self):
        self.base_url = config.INDEED_BASE_URL
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.session = requests.Session()
    
    def search_jobs(self, keywords: str, location: str = "Île-de-France", pages: int = 5) -> List[Dict]:
        """
        Search for jobs on Indeed
        
        Args:
            keywords: Job search keywords (e.g., "Python developer", "Data scientist")
            location: Target location (Île-de-France)
            pages: Number of pages to scrape
        
        Returns:
            List of job postings
        """
        jobs = []
        
        for page in range(pages):
            try:
                # Indeed search URL format
                url = f"{self.base_url}/jobs?q={keywords}&l={location}&start={page * 10}"
                response = self.session.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                job_cards = soup.find_all('div', class_='job_seen_beacon')
                
                for job_card in job_cards:
                    try:
                        job_data = self._extract_job_info(job_card, url)
                        if job_data:
                            jobs.append(job_data)
                    except Exception as e:
                        print(f"Error extracting job: {e}")
                        continue
                
                # Be respectful to the server
                time.sleep(2)
                
            except Exception as e:
                print(f"Error scraping page {page}: {e}")
                continue
        
        return jobs
    
    def _extract_job_info(self, job_card, source_url: str) -> Dict:
        """Extract job information from Indeed job card"""
        try:
            # Job title
            title_elem = job_card.find('h2', class_='jobTitle')
            job_title = title_elem.get_text(strip=True) if title_elem else "N/A"
            
            # Company name
            company_elem = job_card.find('span', class_='companyName')
            company_name = company_elem.get_text(strip=True) if company_elem else "N/A"
            
            # Job URL
            job_link = job_card.find('a', class_='jcs-JobTitle')
            job_url = urljoin(self.base_url, job_link['href']) if job_link else "N/A"
            
            # Location
            location_elem = job_card.find('div', class_='companyLocation')
            location = location_elem.get_text(strip=True) if location_elem else "N/A"
            
            # Job description snippet
            snippet_elem = job_card.find('div', class_='job-snippet')
            description = snippet_elem.get_text(strip=True) if snippet_elem else "N/A"
            
            # Salary (if available)
            salary_elem = job_card.find('span', class_='salary-snippet')
            salary = salary_elem.get_text(strip=True) if salary_elem else None
            
            return {
                'job_id': hash(job_url) % 10**8,
                'company_name': company_name,
                'job_title': job_title,
                'job_url': job_url,
                'job_description': description,
                'location': location,
                'salary': salary,
                'job_board': 'Indeed',
                'posted_date': datetime.utcnow(),
                'source_url': source_url
            }
        except Exception as e:
            print(f"Error in _extract_job_info: {e}")
            return None
    
    def get_job_details(self, job_url: str) -> Dict:
        """Get full job details from job posting page"""
        try:
            response = self.session.get(job_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Full description
            desc_elem = soup.find('div', id='jobDescription')
            full_description = desc_elem.get_text(strip=True) if desc_elem else "N/A"
            
            return {'full_description': full_description}
        except Exception as e:
            print(f"Error getting job details: {e}")
            return {}


class LinkedInScraper:
    """Scraper for LinkedIn job postings"""
    
    def __init__(self):
        self.base_url = config.LINKEDIN_BASE_URL
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def search_jobs(self, keywords: str, location: str = "Île-de-France", pages: int = 3) -> List[Dict]:
        """
        Search for jobs on LinkedIn
        Note: LinkedIn has anti-scraping measures. Consider using LinkedIn API for production.
        
        Args:
            keywords: Job search keywords
            location: Target location
            pages: Number of pages to scrape
        
        Returns:
            List of job postings
        """
        jobs = []
        
        try:
            # LinkedIn search URL
            search_query = keywords.replace(" ", "%20")
            location_query = location.replace(" ", "%20")
            
            # Note: Direct scraping LinkedIn may violate ToS. Use their official API instead.
            print("Note: For production, use LinkedIn's official API instead of scraping.")
            
        except Exception as e:
            print(f"Error searching LinkedIn jobs: {e}")
        
        return jobs


class GlassdoorScraper:
    """Scraper for Glassdoor job postings"""
    
    def __init__(self):
        self.base_url = config.GLASSDOOR_BASE_URL
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def search_jobs(self, keywords: str, location: str = "Île-de-France", pages: int = 3) -> List[Dict]:
        """
        Search for jobs on Glassdoor
        
        Args:
            keywords: Job search keywords
            location: Target location
            pages: Number of pages to scrape
        
        Returns:
            List of job postings
        """
        jobs = []
        
        try:
            print("Glassdoor scraping - Note: Heavy anti-scraping protection. Consider API alternatives.")
            
        except Exception as e:
            print(f"Error searching Glassdoor jobs: {e}")
        
        return jobs
