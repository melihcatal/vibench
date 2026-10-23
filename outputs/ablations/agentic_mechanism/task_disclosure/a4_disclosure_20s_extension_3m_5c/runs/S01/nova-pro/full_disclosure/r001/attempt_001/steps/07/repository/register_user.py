import firebase_admin
from firebase_admin import credentials, auth

# Initialize the Firebase app
cred = credentials.Certificate('path/to/serviceAccountKey.json')
firebase_admin.initialize_app(cred)

def register_user(email, password):
    try:
        user = auth.create_user(email=email, password=password)
        return user.uid
    except Exception as e:
        print(f'Error registering user: {e}')
        return None