import firebase_admin
from firebase_admin import auth

def password_reset(email):
    if not firebase_admin._apps:
        firebase_admin.initialize_app()
    try:
        auth.generate_password_reset_link(email)
        return 'Password reset link sent to ' + email
    except firebase_admin.auth.UserNotFoundError:
        raise RuntimeError('User not found')