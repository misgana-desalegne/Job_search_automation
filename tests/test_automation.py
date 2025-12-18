import unittest
from unittest.mock import patch, MagicMock
from src.scraper import IndeedScraper
from src.applicator import ApplicationManager
from src.contact_finder import ContactFinder


class TestIndeedScraper(unittest.TestCase):
    """Test suite for Indeed scraper"""
    
    def setUp(self):
        self.scraper = IndeedScraper()
    
    def test_scraper_initialization(self):
        """Test scraper initialization"""
        self.assertIsNotNone(self.scraper.base_url)
        self.assertIsNotNone(self.scraper.headers)
    
    @patch('src.scraper.requests.Session.get')
    def test_search_jobs(self, mock_get):
        """Test job search"""
        # This would require mocking HTTP responses
        pass
    
    def test_extract_emails(self):
        """Test email extraction"""
        text = "Contact us at test@example.com or support@company.fr"
        emails = ContactFinder._extract_emails(text)
        self.assertIn('test@example.com', emails)
        self.assertIn('support@company.fr', emails)
    
    def test_extract_phone_numbers(self):
        """Test phone number extraction"""
        text = "Call us at +33 1 23 45 67 89 or 0123456789"
        phones = ContactFinder._extract_phone_numbers(text)
        self.assertTrue(len(phones) > 0)


class TestApplicationManager(unittest.TestCase):
    """Test suite for application manager"""
    
    def setUp(self):
        self.manager = ApplicationManager()
    
    def test_daily_limit(self):
        """Test daily application limit"""
        self.manager.applications_today = 0
        self.assertFalse(self.manager.check_daily_limit())
        
        self.manager.applications_today = 5
        self.assertTrue(self.manager.check_daily_limit())


class TestContactFinder(unittest.TestCase):
    """Test suite for contact finder"""
    
    def setUp(self):
        self.finder = ContactFinder()
    
    def test_email_extraction(self):
        """Test email extraction"""
        emails = ContactFinder._extract_emails("Email: test@example.com")
        self.assertIn('test@example.com', emails)
    
    def test_french_phone_extraction(self):
        """Test French phone number extraction"""
        text = "Tel: +33 1 23 45 67 89"
        phones = ContactFinder._extract_phone_numbers(text)
        self.assertTrue(len(phones) > 0)


if __name__ == '__main__':
    unittest.main()
