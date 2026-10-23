import firebase_admin
from firebase_admin import auth

def register_user(email, password):
    if not firebase_admin._apps:
        firebase_admin.initialize_app()
    user = auth.create_user(email=email, password=password)
    return user.uid