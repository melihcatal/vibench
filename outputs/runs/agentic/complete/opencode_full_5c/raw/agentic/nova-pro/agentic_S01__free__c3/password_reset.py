import firebase_admin
from firebase_admin import auth


def password_reset(email):
    link = auth.generate_password_reset_link(email)
    return link
