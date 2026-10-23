import firebase_admin
from firebase_admin import auth


def email_password_login(email, password):
    user = auth.get_user_by_email(email)
    tokens = auth.create_custom_token(user.uid).decode("utf-8")
    return tokens
