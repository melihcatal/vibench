from firebase_admin import auth, credentials


def email_password_login(email, password):
    user = auth.get_user_by_email(email)
    tokens = auth.create_custom_token(user.uid)
    return tokens.decode("utf-8")
