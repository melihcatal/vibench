import os
import firebase_admin
from firebase_admin import credentials, auth

def initialize_firebase_app():
    if not firebase_admin._apps:
        cred = credentials.Certificate(os.getenv('FIREBASE_ADMIN_CREDENTIALS'))
        firebase_admin.initialize_app(cred)

def get_auth_client():
    initialize_firebase_app()
    return auth