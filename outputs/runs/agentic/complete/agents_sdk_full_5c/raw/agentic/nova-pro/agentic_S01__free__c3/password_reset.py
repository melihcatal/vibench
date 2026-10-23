import os
import firebase_admin
from firebase_admin import auth

cred = firebase_admin.credentials.Certificate('path/to/serviceAccountKey.json')
firebase_admin.initialize_app(cred)

def reset_password(email):
    action_code_settings = auth.ActionCodeSettings(
        url='https://yourapp.com/reset_password?email={email}',
        handle_code_in_app=True)
    auth.generate_password_reset_link(email, action_code_settings)