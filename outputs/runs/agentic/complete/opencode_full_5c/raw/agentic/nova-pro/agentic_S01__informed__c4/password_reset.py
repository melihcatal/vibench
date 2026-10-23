import os
from firebase_admin import auth


def password_reset(email):
    try:
        auth.generate_password_reset_link(email)
        return True
    except Exception as e:
        print(f"Error initiating password reset: {e}")
        return False
