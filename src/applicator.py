import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List
import time
from config.config import config
from src.database import SessionLocal, JobApplication
from datetime import datetime

class ApplicationManager:
    """Manages job applications"""
    
    def __init__(self):
        self.db = SessionLocal()
        self.email_sender = config.EMAIL_ADDRESS
        self.email_password = config.EMAIL_PASSWORD
        self.applications_today = 0
    
    def apply_to_job(self, job_data: Dict, method: str = "email") -> bool:
        """
        Apply to a job posting
        
        Args:
            job_data: Job posting data
            method: Application method (email, online_form, linkedin)
        
        Returns:
            Success status
        """
        try:
            if method == "email":
                success = self._apply_via_email(job_data)
            elif method == "online_form":
                success = self._apply_via_form(job_data)
            elif method == "linkedin":
                success = self._apply_via_linkedin(job_data)
            else:
                return False
            
            if success:
                self._record_application(job_data, method)
                self.applications_today += 1
                return True
            
            return False
        
        except Exception as e:
            print(f"Error applying to job: {e}")
            return False
    
    def _apply_via_email(self, job_data: Dict) -> bool:
        """Apply to job via email"""
        try:
            company_email = job_data.get('company_contact_email')
            if not company_email:
                print(f"No contact email found for {job_data.get('company_name')}")
                return False
            
            # Generate cover letter
            cover_letter = self._generate_cover_letter(job_data)
            
            # Send email
            self._send_email(
                recipient=company_email,
                subject=f"Application for {job_data.get('job_title')} Position",
                body=cover_letter,
                attachments=['resume.pdf', 'cover_letter.pdf']
            )
            
            print(f"✓ Applied to {job_data.get('company_name')} - {job_data.get('job_title')}")
            time.sleep(config.APPLICATION_DELAY_SECONDS)
            return True
        
        except Exception as e:
            print(f"Error in email application: {e}")
            return False
    
    def _apply_via_form(self, job_data: Dict) -> bool:
        """Apply to job via online form (requires Selenium/Playwright)"""
        try:
            # This would require web automation tools like Selenium or Playwright
            # For now, just mark as attempted
            print(f"Form application to {job_data.get('company_name')} (requires automation setup)")
            return False
        
        except Exception as e:
            print(f"Error in form application: {e}")
            return False
    
    def _apply_via_linkedin(self, job_data: Dict) -> bool:
        """Apply to job via LinkedIn"""
        try:
            # This requires LinkedIn authentication and automation
            print(f"LinkedIn application to {job_data.get('company_name')} (requires LinkedIn setup)")
            return False
        
        except Exception as e:
            print(f"Error in LinkedIn application: {e}")
            return False
    
    def _generate_cover_letter(self, job_data: Dict) -> str:
        """Generate personalized cover letter"""
        template = f"""
Dear Hiring Manager,

I am writing to express my strong interest in the {job_data.get('job_title')} position at {job_data.get('company_name')}.

With my relevant experience and skills, I am confident I can make a significant contribution to your team.

Job Details:
- Position: {job_data.get('job_title')}
- Company: {job_data.get('company_name')}
- Location: {job_data.get('location')}

I believe this role aligns perfectly with my career goals and expertise.

Thank you for considering my application. I look forward to the opportunity to discuss how I can contribute to your organization.

Best regards,
[Your Name]
Contact: [Your Email]
Phone: [Your Phone]
        """
        return template.strip()
    
    def _send_email(self, recipient: str, subject: str, body: str, attachments: List[str] = None):
        """Send email with optional attachments"""
        try:
            message = MIMEMultipart()
            message['From'] = self.email_sender
            message['To'] = recipient
            message['Subject'] = subject
            
            message.attach(MIMEText(body, 'plain'))
            
            # Note: Add attachment handling if needed
            
            # Connect to Gmail SMTP
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.email_sender, self.email_password)
                server.send_message(message)
            
            print(f"Email sent to {recipient}")
        
        except Exception as e:
            print(f"Error sending email: {e}")
    
    def _record_application(self, job_data: Dict, method: str):
        """Record application in database"""
        try:
            application = JobApplication(
                job_id=str(job_data.get('job_id')),
                company_name=job_data.get('company_name'),
                job_title=job_data.get('job_title'),
                job_url=job_data.get('job_url'),
                job_description=job_data.get('job_description'),
                location=job_data.get('location'),
                job_board=job_data.get('job_board'),
                date_applied=datetime.utcnow(),
                application_method=method,
                application_status='sent'
            )
            
            self.db.add(application)
            self.db.commit()
            print(f"Application recorded in database")
        
        except Exception as e:
            print(f"Error recording application: {e}")
            self.db.rollback()
    
    def check_daily_limit(self) -> bool:
        """Check if daily application limit has been reached"""
        return self.applications_today >= config.MAX_APPLICATIONS_PER_DAY
    
    def close(self):
        """Close database connection"""
        self.db.close()
