import firebase_admin
from firebase_admin import credentials, auth

def password_reset(email):
    if not firebase_admin._apps:
        cred = credentials.Certificate('path/to/serviceAccountKey.json')
        firebase_admin.initialize_app(cred)
    auth.generate_password_reset_link(email)