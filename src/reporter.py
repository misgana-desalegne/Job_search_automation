import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List
from sqlalchemy import func
from src.database import SessionLocal, JobApplication

class ReportGenerator:
    """Generate reports from application data"""
    
    def __init__(self):
        self.db = SessionLocal()
    
    def generate_all_applications_report(self, output_path: str = "reports/all_applications.xlsx"):
        """Generate report of all applications"""
        try:
            applications = self.db.query(JobApplication).all()
            
            data = []
            for app in applications:
                data.append({
                    'Company Name': app.company_name,
                    'Job Title': app.job_title,
                    'Location': app.location,
                    'Job Board': app.job_board,
                    'Posted Date': app.posted_date,
                    'Date Applied': app.date_applied,
                    'Application Status': app.application_status,
                    'Date Contacted': app.date_contacted,
                    'Response Type': app.response_type,
                    'Interview Scheduled': app.interview_scheduled,
                    'Interview Date': app.interview_date,
                    'Interview Type': app.interview_type,
                    'Company Email': app.company_contact_email,
                    'Company Phone': app.company_contact_phone,
                    'Notes': app.notes
                })
            
            df = pd.DataFrame(data)
            df.to_excel(output_path, index=False)
            print(f"Report generated: {output_path}")
            return df
        
        except Exception as e:
            print(f"Error generating report: {e}")
            return None
    
    def generate_status_summary(self) -> Dict:
        """Generate summary of application statuses"""
        try:
            total = self.db.query(func.count(JobApplication.id)).scalar()
            sent = self.db.query(func.count(JobApplication.id)).filter(JobApplication.application_status == 'sent').scalar()
            pending = self.db.query(func.count(JobApplication.id)).filter(JobApplication.application_status == 'pending').scalar()
            rejected = self.db.query(func.count(JobApplication.id)).filter(JobApplication.application_status == 'rejected').scalar()
            accepted = self.db.query(func.count(JobApplication.id)).filter(JobApplication.application_status == 'accepted').scalar()
            interview = self.db.query(func.count(JobApplication.id)).filter(JobApplication.application_status == 'interview').scalar()
            
            return {
                'Total Applications': total,
                'Sent': sent,
                'Pending Response': pending,
                'Rejected': rejected,
                'Accepted': accepted,
                'Interview Scheduled': interview,
                'Response Rate': f"{(rejected + accepted + interview) / total * 100:.1f}%" if total > 0 else "0%"
            }
        
        except Exception as e:
            print(f"Error generating status summary: {e}")
            return {}
    
    def generate_company_contact_report(self, output_path: str = "reports/company_contacts.xlsx"):
        """Generate report with company contact information"""
        try:
            applications = self.db.query(JobApplication).filter(
                JobApplication.company_contact_email.isnot(None)
            ).all()
            
            data = []
            for app in applications:
                data.append({
                    'Company Name': app.company_name,
                    'Contact Email': app.company_contact_email,
                    'Contact Phone': app.company_contact_phone,
                    'Company Website': app.company_website,
                    'Contact Person': app.contact_person_name,
                    'Contact Title': app.contact_person_title,
                    'Last Updated': app.last_updated
                })
            
            df = pd.DataFrame(data)
            df.to_excel(output_path, index=False)
            print(f"Contact report generated: {output_path}")
            return df
        
        except Exception as e:
            print(f"Error generating contact report: {e}")
            return None
    
    def generate_interview_schedule(self, output_path: str = "reports/interview_schedule.xlsx"):
        """Generate upcoming interview schedule"""
        try:
            upcoming = self.db.query(JobApplication).filter(
                JobApplication.interview_scheduled == True,
                JobApplication.interview_date >= datetime.utcnow()
            ).order_by(JobApplication.interview_date).all()
            
            data = []
            for app in upcoming:
                data.append({
                    'Company Name': app.company_name,
                    'Job Title': app.job_title,
                    'Interview Date': app.interview_date,
                    'Interview Time': app.interview_time,
                    'Interview Type': app.interview_type,
                    'Interview Location': app.interview_location,
                    'Contact Email': app.company_contact_email,
                    'Contact Phone': app.company_contact_phone,
                    'Notes': app.notes
                })
            
            df = pd.DataFrame(data)
            df.to_excel(output_path, index=False)
            print(f"Interview schedule generated: {output_path}")
            return df
        
        except Exception as e:
            print(f"Error generating interview schedule: {e}")
            return None
    
    def generate_weekly_report(self, output_path: str = "reports/weekly_report.xlsx"):
        """Generate weekly statistics"""
        try:
            week_ago = datetime.utcnow() - timedelta(days=7)
            
            applications_this_week = self.db.query(JobApplication).filter(
                JobApplication.date_applied >= week_ago
            ).all()
            
            responses_this_week = self.db.query(JobApplication).filter(
                JobApplication.date_contacted >= week_ago
            ).all()
            
            data = {
                'Week Starting': week_ago.strftime('%Y-%m-%d'),
                'Applications Sent': len(applications_this_week),
                'Responses Received': len(responses_this_week),
                'Response Rate': f"{len(responses_this_week) / len(applications_this_week) * 100:.1f}%" if applications_this_week else "0%",
                'Interviews Scheduled': len([a for a in responses_this_week if a.interview_scheduled]),
                'Rejections': len([a for a in responses_this_week if a.application_status == 'rejected']),
                'Offers': len([a for a in responses_this_week if a.application_status == 'accepted'])
            }
            
            df = pd.DataFrame([data])
            df.to_excel(output_path, index=False)
            print(f"Weekly report generated: {output_path}")
            return df
        
        except Exception as e:
            print(f"Error generating weekly report: {e}")
            return None
    
    def get_application_by_company(self, company_name: str) -> JobApplication:
        """Get application details for a specific company"""
        try:
            return self.db.query(JobApplication).filter(
                JobApplication.company_name == company_name
            ).first()
        except Exception as e:
            print(f"Error retrieving application: {e}")
            return None
    
    def close(self):
        """Close database connection"""
        self.db.close()


def print_status_summary():
    """Print status summary to console"""
    generator = ReportGenerator()
    summary = generator.generate_status_summary()
    
    print("\n" + "="*50)
    print("APPLICATION STATUS SUMMARY")
    print("="*50)
    
    for key, value in summary.items():
        print(f"{key:.<40} {value}")
    
    print("="*50 + "\n")
    generator.close()
