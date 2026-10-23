import os
from firebase_admin import auth, credentials

cred = credentials.Certificate("path/to/serviceAccountKey.json")
app = firebase_admin.initialize_app(cred)

def email_password_login(email, password):
    try:
        user = auth.get_user_by_email(email)
        user = auth.refresh(user.refresh_token)
        return user.id_token
    except Exception as e:
        raise e