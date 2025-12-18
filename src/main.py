import os
import sys
from config.config import config
from src.database import init_db
from src.scraper import IndeedScraper
from src.applicator import ApplicationManager
from src.reporter import ReportGenerator, print_status_summary
from src.contact_finder import ContactFinder
import time

def main():
    """Main application flow"""
    
    print("="*60)
    print("JOB APPLICATION AUTOMATION TOOL - Île-de-France")
    print("="*60)
    
    # Initialize database
    print("\n[1/6] Initializing database...")
    init_db()
    print("✓ Database initialized")
    
    # Search for jobs
    print("\n[2/6] Searching for job postings...")
    scraper = IndeedScraper()
    jobs = scraper.search_jobs(
        keywords="python developer",
        location="Île-de-France",
        pages=2
    )
    print(f"✓ Found {len(jobs)} job postings")
    
    # Enrich job data with contact information
    print("\n[3/6] Finding company contact information...")
    contact_finder = ContactFinder()
    for job in jobs[:min(5, len(jobs))]:  # Process first 5 jobs
        job = contact_finder.enrich_job_posting(job)
        print(f"  ✓ Enriched: {job.get('company_name')}")
        time.sleep(1)  # Be respectful to servers
    
    # Apply to jobs
    print("\n[4/6] Applying to jobs...")
    applicator = ApplicationManager()
    applied_count = 0
    
    for job in jobs[:min(config.MAX_APPLICATIONS_PER_DAY, len(jobs))]:
        if applicator.check_daily_limit():
            print(f"✓ Daily application limit reached ({config.MAX_APPLICATIONS_PER_DAY})")
            break
        
        success = applicator.apply_to_job(job, method="email")
        if success:
            applied_count += 1
            time.sleep(config.APPLICATION_DELAY_SECONDS)
    
    print(f"✓ Applied to {applied_count} jobs")
    applicator.close()
    
    # Generate reports
    print("\n[5/6] Generating reports...")
    
    # Create reports directory if it doesn't exist
    os.makedirs('reports', exist_ok=True)
    
    reporter = ReportGenerator()
    reporter.generate_all_applications_report()
    reporter.generate_company_contact_report()
    reporter.generate_interview_schedule()
    reporter.generate_weekly_report()
    reporter.close()
    print("✓ Reports generated in 'reports/' directory")
    
    # Print summary
    print("\n[6/6] Application Summary")
    print_status_summary()
    
    print("\n" + "="*60)
    print("JOB APPLICATION AUTOMATION COMPLETE")
    print("="*60)
    print("\nGenerated Reports:")
    print("  • reports/all_applications.xlsx - All applications")
    print("  • reports/company_contacts.xlsx - Company contact information")
    print("  • reports/interview_schedule.xlsx - Upcoming interviews")
    print("  • reports/weekly_report.xlsx - Weekly statistics")
    print("\nNext Steps:")
    print("  1. Configure .env file with your credentials")
    print("  2. Add your resume and cover letter templates")
    print("  3. Adjust job search keywords and preferences")
    print("  4. Schedule the automation to run daily")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
