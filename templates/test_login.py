from app import app
from models.models import User, db
from werkzeug.security import check_password_hash

with app.app_context():
    # Test login for existing users
    users = User.query.all()
    print('Testing login for existing users:')
    print('=' * 40)
    
    for user in users:
        print(f'\nUser: {user.username}')
        print(f'Role: {user.role}')
        print(f'Active: {user.is_active}')
        print(f'Password hash: {user.password_hash[:50]}...')
        
        # Test with common passwords
        test_passwords = [user.username, 'password', '123456', 'admin', 'test']
        for pwd in test_passwords:
            if user.check_password(pwd):
                print(f'✓ Password "{pwd}" works!')
                break
        else:
            print('✗ No common passwords work - need to check actual password')
