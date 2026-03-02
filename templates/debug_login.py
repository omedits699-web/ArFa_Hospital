from app import app
from models.models import User, db

with app.app_context():
    print("=== PASSWORD RESET SCRIPT ===")
    
    # Reset passwords to match usernames for testing
    users = User.query.all()
    
    for user in users:
        print(f"\nResetting password for user: {user.username}")
        
        # Set password to username (for testing)
        new_password = user.username
        user.set_password(new_password)
        
        print(f"Password set to: '{new_password}'")
        
        # Test the password
        if user.check_password(new_password):
            print("✓ Password verification successful!")
        else:
            print("✗ Password verification failed!")
    
    # Commit changes
    try:
        db.session.commit()
        print("\n✅ All passwords updated successfully!")
        print("\nYou can now login with:")
        for user in User.query.all():
            print(f"  Username: {user.username}, Password: {user.username}")
    except Exception as e:
        print(f"\n❌ Error updating passwords: {e}")
        db.session.rollback()
