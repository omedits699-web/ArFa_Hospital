#!/usr/bin/env python3
"""
Database Cleanup Script
Clears all registration data (users and patients) while preserving database structure
"""

import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.models import db, User, Patient, Appointment
from datetime import datetime, timedelta

def clear_registration_data():
    """Clear all user and patient registration data"""
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
            
            if user_count == 0 and patient_count == 0:
                print("\n✨ No registration data to clear!")
                return
            
            # Confirm deletion
            print(f"\n⚠️  This will delete ALL {user_count} users and {patient_count} patients!")
            confirm = input("Are you sure you want to continue? (type 'yes' to confirm): ")
            
            if confirm.lower() != 'yes':
                print("❌ Operation cancelled")
                return
            
            print("\n🧹 Clearing registration data...")
            
            # Delete all users (this will cascade if foreign keys are set)
            deleted_users = User.query.delete()
            print(f"   Deleted {deleted_users} users")
            
            # Delete all patients
            deleted_patients = Patient.query.delete()
            print(f"   Deleted {deleted_patients} patients")
            
            # Optionally clear appointments too (uncomment if needed)
            # deleted_appointments = Appointment.query.delete()
            # print(f"   Deleted {deleted_appointments} appointments")
            
            # Commit changes
            db.session.commit()
            print("✅ Database cleared successfully!")
            
            # Verify deletion
            remaining_users = User.query.count()
            remaining_patients = Patient.query.count()
            
            print(f"\n📊 Updated Database Status:")
            print(f"   Users: {remaining_users}")
            print(f"   Patients: {remaining_patients}")
            
            if remaining_users == 0 and remaining_patients == 0:
                print("🎉 All registration data has been cleared!")
            else:
                print("⚠️  Some data may remain - check foreign key constraints")
                
        except Exception as e:
            print(f"❌ Error clearing database: {e}")
            db.session.rollback()
            raise

def reset_database_completely():
    """Completely reset database (delete and recreate)"""
    app = Flask(__name__)
    
    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/hospital.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        try:
            print("🔨 Completely resetting database...")
            
            # Drop all tables
            db.drop_all()
            print("   Dropped all tables")
            
            # Recreate all tables
            db.create_all()
            print("   Recreated all tables")
            
            print("✅ Database reset successfully!")
            
        except Exception as e:
            print(f"❌ Error resetting database: {e}")
            raise

def clear_old_patient_data():
    """Clear patient registration data older than 40 years"""
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
            
            # Calculate cutoff date (40 years ago from today)
            cutoff_date = datetime.now() - timedelta(days=40*365)
            print(f"📅 Cutoff date: {cutoff_date.strftime('%Y-%m-%d')}")
            
            # Count records before deletion
            total_users = User.query.count()
            total_patients = Patient.query.count()
            total_appointments = Appointment.query.count()
            
            # Find old users (older than 40 years)
            old_users = User.query.filter(User.created_at < cutoff_date).all()
            old_user_ids = [user.id for user in old_users]
            
            # Find old patients (older than 40 years)
            old_patients = Patient.query.filter(Patient.created_at < cutoff_date).all()
            
            # Find old appointments (older than 40 years)
            old_appointments = Appointment.query.filter(Appointment.created_at < cutoff_date).all()
            
            print(f"\n📊 Current Database Status:")
            print(f"   Total Users: {total_users}")
            print(f"   Total Patients: {total_patients}")
            print(f"   Total Appointments: {total_appointments}")
            print(f"   Users older than 40 years: {len(old_users)}")
            
            if len(old_users) == 0 and len(old_patients) == 0:
                print("\n✨ No old registration data to clear!")
                return
            
            # Confirm deletion
            print(f"\n⚠️  This will delete:")
            print(f"   - {len(old_users)} users registered before {cutoff_date.strftime('%Y-%m-%d')}")
            print(f"   - {len(old_patients)} patient records")
            print(f"   - {len(old_appointments)} appointment records")
            confirm = input("Are you sure you want to continue? (type 'yes' to confirm): ")
            
            if confirm.lower() != 'yes':
                print("❌ Operation cancelled")
                return
            
            print("\n🧹 Clearing old registration data...")
            
            # Delete old appointments first (to avoid foreign key constraints)
            deleted_appointments = len(old_appointments)
            for appointment in old_appointments:
                db.session.delete(appointment)
            print(f"   Deleted {deleted_appointments} appointments")
            
            # Delete old patients
            deleted_patients = len(old_patients)
            for patient in old_patients:
                db.session.delete(patient)
            print(f"   Deleted {deleted_patients} patients")
            
            # Delete old users
            deleted_users = len(old_users)
            for user in old_users:
                db.session.delete(user)
            print(f"   Deleted {deleted_users} users")
            
            # Commit changes
            db.session.commit()
            print("✅ Old registration data cleared successfully!")
            
            # Verify deletion
            remaining_users = User.query.count()
            remaining_patients = Patient.query.count()
            remaining_appointments = Appointment.query.count()
            
            print(f"\n📊 Updated Database Status:")
            print(f"   Users: {remaining_users}")
            print(f"   Patients: {remaining_patients}")
            print(f"   Appointments: {remaining_appointments}")
            
            print("🎉 Old registration data has been cleared!")
                
        except Exception as e:
            print(f"❌ Error clearing old data: {e}")
            db.session.rollback()
            raise

def renew_database_structure():
    """Renew database structure while preserving recent data"""
    app = Flask(__name__)
    
    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/hospital.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        try:
            print("🔄 Renewing database structure...")
            
            # Backup recent data (last 40 years)
            cutoff_date = datetime.now() - timedelta(days=40*365)
            
            # Get recent data
            recent_users = User.query.filter(User.created_at >= cutoff_date).all()
            recent_patients = Patient.query.filter(Patient.created_at >= cutoff_date).all()
            recent_appointments = Appointment.query.filter(Appointment.created_at >= cutoff_date).all()
            
            print(f"   Backing up {len(recent_users)} recent users")
            print(f"   Backing up {len(recent_patients)} patients")
            print(f"   Backing up {len(recent_appointments)} appointments")
            
            # Drop and recreate tables
            db.drop_all()
            print("   Dropped all tables")
            
            db.create_all()
            print("   Recreated all tables")
            
            # Restore recent data
            for user in recent_users:
                db.session.add(user)
            
            for patient in recent_patients:
                db.session.add(patient)
            
            for appointment in recent_appointments:
                db.session.add(appointment)
            
            db.session.commit()
            print("   Restored recent data")
            
            print("✅ Database renewed successfully!")
            
        except Exception as e:
            print(f"❌ Error renewing database: {e}")
            db.session.rollback()
            raise

if __name__ == "__main__":
    print("🏥 Hospital Database Cleanup Tool")
    print("=" * 40)
    
    choice = input("Choose an option:\n1. Clear registration data only\n2. Completely reset database\n3. Clear patient data older than 40 years\n4. Renew database structure (keep recent 40 years)\nEnter choice (1, 2, 3, or 4): ")
    
    if choice == "1":
        clear_registration_data()
    elif choice == "2":
        reset_database_completely()
    elif choice == "3":
        clear_old_patient_data()
    elif choice == "4":
        renew_database_structure()
    else:
        print("❌ Invalid choice")
