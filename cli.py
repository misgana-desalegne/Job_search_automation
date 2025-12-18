"""
Command-line interface for managing job applications
"""

import argparse
import sys
from datetime import datetime, timedelta
from src.scraper import IndeedScraper, LinkedInScraper, GlassdoorScraper
from src.applicator import ApplicationManager
from src.reporter import ReportGenerator, print_status_summary
from src.contact_finder import ContactFinder
from src.database import SessionLocal, JobApplication, init_db


def cmd_search(args):
    """Search for job postings"""
    print(f"\n📋 Searching for {args.keyword} jobs in {args.location}...")
    
    scraper = IndeedScraper()
    jobs = scraper.search_jobs(
        keywords=args.keyword,
        location=args.location,
        pages=args.pages
    )
    
    print(f"\n✓ Found {len(jobs)} jobs:\n")
    
    for i, job in enumerate(jobs, 1):
        print(f"{i}. {job.get('job_title')} at {job.get('company_name')}")
        print(f"   Location: {job.get('location')}")
        print(f"   URL: {job.get('job_url')}\n")
    
    return jobs


def cmd_apply(args):
    """Apply to jobs"""
    if not args.company:
        print("Error: --company is required for applying")
        return False
    
    manager = ApplicationManager()
    
    db = SessionLocal()
    job = db.query(JobApplication).filter_by(company_name=args.company).first()
    
    if not job:
        print(f"Error: No job found for {args.company}")
        return False
    
    job_data = {
        'job_id': job.job_id,
        'company_name': job.company_name,
        'job_title': job.job_title,
        'job_url': job.job_url,
        'location': job.location,
        'company_contact_email': job.company_contact_email
    }
    
    success = manager.apply_to_job(job_data, method=args.method)
    manager.close()
    db.close()
    
    if success:
        print(f"✓ Application sent to {args.company}")
    else:
        print(f"✗ Failed to apply to {args.company}")
    
    return success


def cmd_report(args):
    """Generate reports"""
    reporter = ReportGenerator()
    
    print("\n📊 Generating reports...\n")
    
    if args.type == 'all' or args.type == 'applications':
        reporter.generate_all_applications_report()
    
    if args.type == 'all' or args.type == 'contacts':
        reporter.generate_company_contact_report()
    
    if args.type == 'all' or args.type == 'interviews':
        reporter.generate_interview_schedule()
    
    if args.type == 'all' or args.type == 'weekly':
        reporter.generate_weekly_report()
    
    if args.type == 'all' or args.type == 'summary':
        print_status_summary()
    
    reporter.close()


def cmd_status(args):
    """Show application status summary"""
    print_status_summary()


def cmd_track(args):
    """Track application status for a company"""
    db = SessionLocal()
    job = db.query(JobApplication).filter_by(company_name=args.company).first()
    
    if not job:
        print(f"No application found for {args.company}")
        db.close()
        return
    
    print(f"\n{'='*60}")
    print(f"APPLICATION DETAILS: {job.company_name}")
    print(f"{'='*60}")
    print(f"Job Title: {job.job_title}")
    print(f"Location: {job.location}")
    print(f"Job Board: {job.job_board}")
    print(f"Posted: {job.posted_date}")
    print(f"\nAPPLICATION STATUS:")
    print(f"Date Applied: {job.date_applied}")
    print(f"Status: {job.application_status}")
    print(f"Method: {job.application_method}")
    print(f"\nRESPONSE:")
    print(f"Date Contacted: {job.date_contacted}")
    print(f"Response Type: {job.response_type}")
    print(f"Response: {job.response_content or 'N/A'}")
    print(f"\nINTERVIEW:")
    print(f"Scheduled: {job.interview_scheduled}")
    print(f"Date: {job.interview_date}")
    print(f"Time: {job.interview_time}")
    print(f"Type: {job.interview_type}")
    print(f"Location: {job.interview_location or 'N/A'}")
    print(f"\nNOTES:")
    print(f"{job.notes or 'No notes'}")
    print(f"{'='*60}\n")
    
    db.close()


def cmd_contact(args):
    """Find company contact information"""
    finder = ContactFinder()
    info = finder.find_company_info(args.company, args.website)
    
    print(f"\n📞 CONTACT INFORMATION: {args.company}")
    print(f"{'='*60}")
    print(f"Email: {info.get('email', 'Not found')}")
    print(f"Phone: {info.get('phone', 'Not found')}")
    print(f"Website: {info.get('website', 'Not found')}")
    print(f"Has Contact Page: {info.get('has_contact_page', 'Unknown')}")
    print(f"{'='*60}\n")


def cmd_init_db(args):
    """Initialize database"""
    print("Initializing database...")
    init_db()
    print("✓ Database initialized")


def main():
    parser = argparse.ArgumentParser(
        description='Job Application Automation Tool'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search for jobs')
    search_parser.add_argument('keyword', help='Job keyword')
    search_parser.add_argument('--location', default='Île-de-France', help='Location')
    search_parser.add_argument('--pages', type=int, default=3, help='Number of pages')
    search_parser.set_defaults(func=cmd_search)
    
    # Apply command
    apply_parser = subparsers.add_parser('apply', help='Apply to a job')
    apply_parser.add_argument('--company', required=True, help='Company name')
    apply_parser.add_argument('--method', default='email', choices=['email', 'form', 'linkedin'])
    apply_parser.set_defaults(func=cmd_apply)
    
    # Report command
    report_parser = subparsers.add_parser('report', help='Generate reports')
    report_parser.add_argument(
        '--type',
        default='all',
        choices=['all', 'applications', 'contacts', 'interviews', 'weekly', 'summary']
    )
    report_parser.set_defaults(func=cmd_report)
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Show status summary')
    status_parser.set_defaults(func=cmd_status)
    
    # Track command
    track_parser = subparsers.add_parser('track', help='Track specific application')
    track_parser.add_argument('company', help='Company name')
    track_parser.set_defaults(func=cmd_track)
    
    # Contact command
    contact_parser = subparsers.add_parser('contact', help='Find contact information')
    contact_parser.add_argument('company', help='Company name')
    contact_parser.add_argument('--website', help='Company website')
    contact_parser.set_defaults(func=cmd_contact)
    
    # Init DB command
    init_parser = subparsers.add_parser('init', help='Initialize database')
    init_parser.set_defaults(func=cmd_init_db)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    args.func(args)


if __name__ == '__main__':
    main()
