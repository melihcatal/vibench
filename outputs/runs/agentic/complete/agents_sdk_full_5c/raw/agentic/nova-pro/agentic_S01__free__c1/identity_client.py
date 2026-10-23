import os
import firebase_admin
from firebase_admin import credentials, auth

def initialize_app():
    if not firebase_admin._apps:
        cred = credentials.Certificate(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
        firebase_admin.initialize_app(cred)

def get_auth_client():
    initialize_app()
    return auth