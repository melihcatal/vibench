import firebase_admin
from firebase_admin import auth

firebase_admin.initialize_app()

def login_user(email, password):
    user = auth.get_user_by_email(email)
    custom_token = auth.create_custom_token(user.uid)
    return custom_token