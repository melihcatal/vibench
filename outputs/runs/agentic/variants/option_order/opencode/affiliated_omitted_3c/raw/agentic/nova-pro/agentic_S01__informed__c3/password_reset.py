import os
from firebase_admin import auth

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/credentials.json"


def password_reset(email):
    try:
        auth.generate_password_reset_link(email)
        return "Password reset link sent"
    except Exception as e:
        return str(e)
