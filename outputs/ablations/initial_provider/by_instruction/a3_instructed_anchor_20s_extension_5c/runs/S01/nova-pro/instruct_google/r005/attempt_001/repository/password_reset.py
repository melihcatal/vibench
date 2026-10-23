import firebase_admin
from firebase_admin import auth

def password_reset(email):
    if not firebase_admin._apps:
        firebase_admin.initialize_app()
    auth.generate_password_reset_link(email)