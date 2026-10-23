import firebase_admin
from firebase_admin import credentials, auth

# Initialize the app with a service account, granting admin privileges
cred = credentials.Certificate('path/to/serviceAccountKey.json')
firebase_admin.initialize_app(cred)

def register_user(email, password):
    try:
        user = auth.create_user(email=email, password=password)
        print(f'Successfully registered user with uid: {user.uid}')
    except Exception as e:
        print(f'Error registering user: {e}')

# Example usage
# register_user('user@example.com', 'strongPassword123')