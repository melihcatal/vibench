import firebase_admin
from firebase_admin import auth

def initialize_app():
    if not firebase_admin._apps:
        firebase_admin.initialize_app()