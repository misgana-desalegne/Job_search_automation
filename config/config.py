import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration"""
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./applications.db")
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    
    # Scraping settings
    LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
    LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")
    
    # Application settings
    MAX_APPLICATIONS_PER_DAY = int(os.getenv("MAX_APPLICATIONS_PER_DAY", 5))
    APPLICATION_DELAY_SECONDS = int(os.getenv("APPLICATION_DELAY_SECONDS", 10))
    HEADLESS_BROWSER = os.getenv("HEADLESS_BROWSER", "true").lower() == "true"
    
    # Target location
    TARGET_REGION = os.getenv("TARGET_REGION", "Île-de-France")
    TARGET_CITIES = os.getenv("TARGET_CITIES", "Paris").split(",")
    
    # Base URLs
    INDEED_BASE_URL = "https://www.indeed.com"
    LINKEDIN_BASE_URL = "https://www.linkedin.com"
    GLASSDOOR_BASE_URL = "https://www.glassdoor.com"

config = Config()
