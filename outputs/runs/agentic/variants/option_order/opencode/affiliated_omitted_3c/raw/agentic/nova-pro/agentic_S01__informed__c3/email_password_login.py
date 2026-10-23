import os
from firebase_admin import auth

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/credentials.json"


def email_password_login(email, password):
    try:
        user = auth.get_user_by_email(email)
        custom_token = auth.create_custom_token(user.uid)
        return custom_token
    except Exception as e:
        return str(e)
