import firebase_admin
from firebase_admin import auth

firebase_admin.initialize_app()

def register_user(email, password):
    user = auth.create_user(email=email, password=password)
    return user.uid