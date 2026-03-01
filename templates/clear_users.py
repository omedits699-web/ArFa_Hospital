#!/usr/bin/env python3
"""
Clear all existing user registrations
"""

import os
import sys
from flask import Flask

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.models import db, User, Patient, Appointment

def clear_all_users():
    """Clear all user registration data"""
    app = Flask(__name__)
    
    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/hospital.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        try:
            print("🗂️  Connecting to database...")
            
            # Check database connection
            db.engine.execute("SELECT 1")
            print("✅ Database connected successfully")
            
            # Count records before deletion
            user_count = User.query.count()
            patient_count = Patient.query.count()
            appointment_count = Appointment.query.count()
            
            print(f"\n📊 Current Database Status:")
            print(f"   Users: {user_count}")
            print(f"   Patients: {patient_count}")
            print(f"   Appointments: {appointment_count}")
            
            if user_count == 0:
                print("\n✨ No users to clear!")
                return
            
            print(f"\n⚠️  This will delete ALL {user_count} users and related data!")
            print("Type 'DELETE' to confirm:")
            confirm = input("Confirm: ")
            
            if confirm != 'DELETE':
                print("❌ Operation cancelled")
                return
            
            print("\n🧹 Clearing all user data...")
            
            # Delete all appointments first (to avoid foreign key constraints)
            deleted_appointments = Appointment.query.delete()
            print(f"   Deleted {deleted_appointments} appointments")
            
            # Delete all patients
            deleted_patients = Patient.query.delete()
            print(f"   Deleted {deleted_patients} patients")
            
            # Delete all users
            deleted_users = User.query.delete()
            print(f"   Deleted {deleted_users} users")
            
            # Commit changes
            db.session.commit()
            print("✅ All user data cleared successfully!")
            
            # Verify deletion
            remaining_users = User.query.count()
            remaining_patients = Patient.query.count()
            remaining_appointments = Appointment.query.count()
            
            print(f"\n📊 Updated Database Status:")
            print(f"   Users: {remaining_users}")
            print(f"   Patients: {remaining_patients}")
            print(f"   Appointments: {remaining_appointments}")
            
            print("🎉 Database is now ready for fresh registrations!")
                
        except Exception as e:
            print(f"❌ Error clearing data: {e}")
            db.session.rollback()
            raise

if __name__ == "__main__":
    print("🏥 Clear All User Registrations")
    print("=" * 40)
    clear_all_users()
