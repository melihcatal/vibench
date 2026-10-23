import os
import firebase_admin
from firebase_admin import auth

cred = firebase_admin.credentials.Certificate('path/to/serviceAccountKey.json')
firebase_admin.initialize_app(cred)

def login_user(email, password):
    user = auth.get_user_by_email(email)
    custom_token = auth.create_custom_token(user.uid)
    return custom_token