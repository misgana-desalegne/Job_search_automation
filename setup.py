"""
Update script to initialize the application
Handles database setup and initial configuration
"""

import os
import sys
from pathlib import Path

def setup_project():
    """Initialize project structure and dependencies"""
    
    print("="*60)
    print("JOB APPLICATION AUTOMATION - SETUP")
    print("="*60)
    
    # Create necessary directories
    print("\n[1/3] Creating project directories...")
    directories = ['reports', 'logs', 'data', 'config']
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  ✓ Created {directory}/")
    
    # Create .env file if it doesn't exist
    print("\n[2/3] Setting up environment configuration...")
    env_file = 'config/.env'
    env_example = 'config/.env.example'
    
    if not os.path.exists(env_file) and os.path.exists(env_example):
        with open(env_example, 'r') as f:
            example_content = f.read()
        with open(env_file, 'w') as f:
            f.write(example_content)
        print(f"  ✓ Created {env_file}")
        print("  ⚠️  Please update .env with your credentials!")
    
    # Initialize database
    print("\n[3/3] Initializing database...")
    try:
        from src.database import init_db
        init_db()
        print("  ✓ Database initialized")
    except Exception as e:
        print(f"  ✗ Error initializing database: {e}")
        return False
    
    print("\n" + "="*60)
    print("SETUP COMPLETE!")
    print("="*60)
    print("\nNext Steps:")
    print("1. Edit config/.env with your credentials")
    print("2. Add resume and cover letter templates to data/")
    print("3. Run: python src/main.py")
    print("\nFor help, see README.md")
    
    return True


if __name__ == "__main__":
    success = setup_project()
    sys.exit(0 if success else 1)
