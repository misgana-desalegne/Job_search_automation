from sqlalchemy import create_engine, Column, String, DateTime, Integer, Text, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from config.config import config

# Create database engine
engine = create_engine(config.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class JobApplication(Base):
    """Database model for job applications"""
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, unique=True, index=True)
    company_name = Column(String, index=True)
    job_title = Column(String, index=True)
    job_url = Column(String, unique=True)
    job_description = Column(Text)
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)
    location = Column(String, index=True)
    job_board = Column(String)  # Indeed, LinkedIn, Glassdoor, etc.
    posted_date = Column(DateTime, default=datetime.utcnow)
    
    # Contact information
    company_contact_email = Column(String, nullable=True)
    company_contact_phone = Column(String, nullable=True)
    company_website = Column(String, nullable=True)
    contact_person_name = Column(String, nullable=True)
    contact_person_title = Column(String, nullable=True)
    contact_person_email = Column(String, nullable=True)
    
    # Application tracking
    date_applied = Column(DateTime, nullable=True)
    application_method = Column(String)  # online_form, email, linkedin
    application_status = Column(String, default="pending")  # pending, sent, rejected, accepted, interview
    
    # Response tracking
    date_contacted = Column(DateTime, nullable=True)
    response_type = Column(String, nullable=True)  # email, phone, linkedin, website
    response_content = Column(Text, nullable=True)
    
    # Interview details
    interview_scheduled = Column(Boolean, default=False)
    interview_date = Column(DateTime, nullable=True)
    interview_time = Column(String, nullable=True)
    interview_type = Column(String, nullable=True)  # phone, video, in_person
    interview_location = Column(String, nullable=True)
    
    # Feedback and notes
    notes = Column(Text, nullable=True)
    feedback = Column(Text, nullable=True)
    rejection_reason = Column(String, nullable=True)
    
    # Last updated
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

def get_db():
    """Database dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database"""
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()
