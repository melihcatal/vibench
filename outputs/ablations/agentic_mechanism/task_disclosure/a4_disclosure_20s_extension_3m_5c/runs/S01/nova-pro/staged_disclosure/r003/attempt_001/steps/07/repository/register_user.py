import firebase_admin
from firebase_admin import auth

if not firebase_admin._apps:
    firebase_admin.initialize_app()

def register_user(email, password):
    try:
        user = auth.create_user(email=email, password=password)
        print(f'Successfully created new user: {user.uid}')
    except Exception as e:
        print(f'Error creating user: {e}')

# Example usage:
# register_user('user@example.com', 'strongPassword123')