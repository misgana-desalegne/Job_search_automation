# Job Application Automation Tool

A comprehensive Python automation tool to scrape job postings in Île-de-France, apply to relevant positions, and generate detailed reports.

## Features

✨ **Web Scraping**
- Scrapes job postings from Indeed, LinkedIn, and Glassdoor
- Filters by location (Île-de-France region)
- Supports multiple job boards and keywords

📧 **Automated Applications**
- Sends personalized applications via email
- Tracks application status
- Implements application throttling (5 per day by default)
- Generates customized cover letters

🔍 **Contact Information**
- Finds company contact details
- Extracts email addresses and phone numbers
- Discovers company websites
- Locates decision-maker information

📊 **Comprehensive Reporting**
- All applications with full details
- Company contact information database
- Interview schedule
- Weekly statistics
- Response rate tracking
- Application status summary

## Project Structure

```
JobapplicationAutomation/
├── config/
│   ├── config.py              # Configuration management
│   └── .env.example           # Environment variables template
├── src/
│   ├── main.py               # Main application entry point
│   ├── database.py           # SQLAlchemy models & DB setup
│   ├── scraper.py            # Web scrapers (Indeed, LinkedIn, Glassdoor)
│   ├── applicator.py         # Job application logic
│   ├── reporter.py           # Report generation
│   └── contact_finder.py     # Company contact discovery
├── tests/
│   └── test_automation.py    # Unit tests
├── reports/                  # Generated reports (Excel files)
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Gmail account (for email applications)
- Gmail App Password (not regular password)

### Setup Steps

1. **Clone/Extract the project**
   ```bash
   cd JobapplicationAutomation
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy the example file
   cp config/.env.example config/.env
   
   # Edit config/.env with your settings
   ```

5. **Initialize the database**
   ```bash
   python -c "from src.database import init_db; init_db()"
   ```

## Configuration

Edit `config/.env` with your settings:

```env
# Email Configuration (Gmail)
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

# Database
DATABASE_URL=sqlite:///./applications.db

# LinkedIn Credentials (for LinkedIn scraping)
LINKEDIN_EMAIL=your_email@gmail.com
LINKEDIN_PASSWORD=your_password

# Application Settings
MAX_APPLICATIONS_PER_DAY=5
APPLICATION_DELAY_SECONDS=10
HEADLESS_BROWSER=true

# Target Location
TARGET_REGION=Île-de-France
TARGET_CITIES=Paris,Boulogne-Billancourt,Saint-Denis
```

### Gmail App Password Setup

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable "2-Step Verification"
3. Go to App Passwords
4. Select "Mail" and "Windows Computer"
5. Copy the generated 16-character password
6. Use this in `EMAIL_PASSWORD` in .env

## Usage

### Run the main automation
```bash
python src/main.py
```

### Generate reports only
```bash
python -c "from src.reporter import ReportGenerator; r = ReportGenerator(); r.generate_all_applications_report()"
```

### Check application status
```bash
python -c "from src.reporter import print_status_summary; print_status_summary()"
```

### Run tests
```bash
python -m pytest tests/
# or
python -m unittest tests.test_automation
```

## Database Schema

### JobApplication Table
```
- id: Unique identifier
- company_name: Company name
- job_title: Job position title
- job_url: Link to job posting
- location: Job location
- job_board: Source (Indeed, LinkedIn, etc.)
- date_applied: When application was sent
- application_status: pending, sent, rejected, accepted, interview
- company_contact_email: Company email
- company_contact_phone: Company phone
- interview_scheduled: Boolean flag
- interview_date: Scheduled interview date
- interview_time: Interview time
- interview_type: phone, video, in_person
- notes: Custom notes
- feedback: Company feedback
- last_updated: Last modification date
```

## Reports Generated

### 1. all_applications.xlsx
Complete list of all applications with:
- Company name
- Job title
- Location
- Application status
- Date applied
- Response information
- Interview details

### 2. company_contacts.xlsx
Database of company contact information:
- Company name
- Email address
- Phone number
- Website
- Contact person details

### 3. interview_schedule.xlsx
Upcoming interviews:
- Company name
- Interview date & time
- Interview type
- Interview location
- Contact information

### 4. weekly_report.xlsx
Weekly statistics:
- Applications sent
- Responses received
- Response rate
- Interviews scheduled
- Rejections
- Job offers

## Advanced Features

### Custom Job Search
```python
from src.scraper import IndeedScraper

scraper = IndeedScraper()
jobs = scraper.search_jobs(
    keywords="Data Science",
    location="Île-de-France",
    pages=5
)
```

### Contact Enrichment
```python
from src.contact_finder import ContactFinder

finder = ContactFinder()
enriched_job = finder.enrich_job_posting(job_data)
```

### Track Interview
```python
from src.database import SessionLocal, JobApplication
from datetime import datetime, timedelta

db = SessionLocal()
app = db.query(JobApplication).filter_by(company_name="CompanyName").first()
app.interview_scheduled = True
app.interview_date = datetime.utcnow() + timedelta(days=5)
app.interview_type = "video"
db.commit()
```

## Scheduling (Automated Daily Runs)

### Windows Task Scheduler
```batch
# Create a batch file run_automation.bat
@echo off
cd C:\Users\misga\OneDrive\Desktop\JobapplicationAutomation
venv\Scripts\python.exe src/main.py
```

Then schedule it in Task Scheduler to run daily.

### Linux/macOS Cron
```bash
0 9 * * * cd /path/to/JobapplicationAutomation && /path/to/venv/bin/python src/main.py
```

## Best Practices

1. **Rate Limiting**: Respect website terms of service
   - Default: 5 applications per day
   - 10-second delay between applications
   - Adjust based on your comfort level

2. **Email Templates**: Customize cover letters
   - Edit `_generate_cover_letter()` in applicator.py
   - Make templates more personalized

3. **Database Backups**: Regularly backup applications.db
   - Contains all your application history
   - Review before automated runs

4. **Monitor Applications**: Check reports weekly
   - Track response rates
   - Identify successful job boards
   - Optimize search keywords

5. **Legal Considerations**:
   - Verify website scraping is allowed (check robots.txt)
   - Some sites prohibit automated scraping
   - Always read Terms of Service

## Troubleshooting

### Email not sending
- Verify Gmail App Password is correct
- Check 2-Step Verification is enabled
- Ensure SMTP access is allowed

### No jobs found
- Check target location spelling
- Verify internet connection
- Try different keywords
- Check job board availability

### Database errors
- Delete applications.db to reset
- Run `init_db()` again
- Check database path in .env

### LinkedIn authentication fails
- Update credentials in .env
- Consider using LinkedIn API instead
- Note: LinkedIn prohibits scraping

## Future Enhancements

- [ ] Integration with LinkedIn API
- [ ] AI-powered cover letter generation
- [ ] Interview preparation materials
- [ ] Salary negotiation tracking
- [ ] Job matching algorithm
- [ ] Web dashboard for monitoring
- [ ] Slack/Email notifications
- [ ] Mobile application

## Legal & Ethical Notes

⚠️ **Important:**
- Only scrape websites that allow it (check robots.txt)
- Respect rate limits and terms of service
- Don't use for spam or harassment
- Obtain proper authorization for data collection
- Consider using official APIs when available
- Follow GDPR and local data protection laws

## Support & Contributing

For issues, feature requests, or contributions:
1. Check existing documentation
2. Review database schema
3. Test with sample data first
4. Submit detailed bug reports

## License

This project is for personal use. Ensure compliance with job board terms of service.

## Contact

For questions or support, refer to configuration documentation or project README.

---

**Happy job hunting! 🚀**
