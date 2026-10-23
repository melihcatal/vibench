import os
from firebase_admin import auth


def email_password_login(email, password):
    try:
        user = auth.get_user_by_email(email)
        tokens = auth.create_custom_token(user.uid)
        return tokens
    except Exception as e:
        print(f"Error logging in: {e}")
        return None
