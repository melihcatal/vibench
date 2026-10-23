import firebase_admin
from firebase_admin import auth

def sign_in_with_email_and_password(email, password):
    if not firebase_admin._apps:
        firebase_admin.initialize_app()
    try:
        user = auth.get_user_by_email(email)
        user = auth.sign_in_with_email_and_password(email, password)
        return user.id_token, user.refresh_token
    except firebase_admin.auth.UserNotFoundError:
        return None, None