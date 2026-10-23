from firebase_admin import auth, credentials


def password_reset(email):
    link = auth.generate_password_reset_link(email)
    return link
