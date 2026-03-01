#!/usr/bin/env python3
"""
Remove specific username from database
"""

import os
import sys
from flask import Flask

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.models import db, User, Patient, Appointment

def remove_specific_username():
    """Remove a specific username and all related data"""
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
            
            # Show all current users
            users = User.query.all()
            print(f"\n📊 Current Users:")
            for user in users:
                print(f"   ID: {user.id}, Username: '{user.username}', Role: {user.role}")
            
            if not users:
                print("\n✨ No users found in database!")
                return
            
            # Get username to remove
            username_to_remove = input("\nEnter username to remove: ").strip()
            
            if not username_to_remove:
                print("❌ No username provided")
                return
            
            # Find the user
            user_to_remove = User.query.filter_by(username=username_to_remove).first()
            
            if not user_to_remove:
                print(f"❌ User '{username_to_remove}' not found!")
                return
            
            print(f"\n⚠️  Found user: {user_to_remove.username} (ID: {user_to_remove.id}, Role: {user_to_remove.role})")
            
            # Confirm deletion
            confirm = input(f"Type 'DELETE' to remove user '{username_to_remove}' and ALL related data: ")
            
            if confirm != 'DELETE':
                print("❌ Operation cancelled")
                return
            
            print(f"\n🧹 Removing user '{username_to_remove}' and related data...")
            
            # Count related data before deletion
            patient_count = Patient.query.filter_by(name=username_to_remove).count()
            appointment_count = Appointment.query.filter_by(patient_name=username_to_remove).count()
            
            print(f"   Found {patient_count} patient records")
            print(f"   Found {appointment_count} appointment records")
            
            # Delete related appointments first
            deleted_appointments = Appointment.query.filter_by(patient_name=username_to_remove).delete()
            print(f"   Deleted {deleted_appointments} appointments")
            
            # Delete related patient records
            deleted_patients = Patient.query.filter_by(name=username_to_remove).delete()
            print(f"   Deleted {deleted_patients} patient records")
            
            # Delete the user
            deleted_users = User.query.filter_by(username=username_to_remove).delete()
            print(f"   Deleted {deleted_users} user records")
            
            # Commit changes
            db.session.commit()
            print("✅ User and all related data removed successfully!")
            
            # Show remaining users
            remaining_users = User.query.all()
            print(f"\n📊 Remaining Users ({len(remaining_users)}):")
            for user in remaining_users:
                print(f"   ID: {user.id}, Username: '{user.username}', Role: {user.role}")
                
        except Exception as e:
            print(f"❌ Error removing user: {e}")
            db.session.rollback()
            raise

if __name__ == "__main__":
    print("🏥 Remove Specific Username")
    print("=" * 40)
    remove_specific_username()
