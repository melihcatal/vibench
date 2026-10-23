import firebase_admin
from firebase_admin import auth

# Initialize the Firebase Admin SDK
def initialize_app():
    if not firebase_admin._apps:
        firebase_admin.initialize_app({
            'credential': firebase_admin.credential.Certificate('path/to/serviceAccountKey.json'),
            'databaseURL': 'https://<DATABASE_NAME>.firebaseio.com'
        })

# Utility functions for account lifecycle management
def create_user(email, password):
    return auth.create_user(email=email, password=password)

def delete_user(uid):
    return auth.delete_user(uid)

def update_password(uid, new_password):
    return auth.update_user(uid, password=new_password)
