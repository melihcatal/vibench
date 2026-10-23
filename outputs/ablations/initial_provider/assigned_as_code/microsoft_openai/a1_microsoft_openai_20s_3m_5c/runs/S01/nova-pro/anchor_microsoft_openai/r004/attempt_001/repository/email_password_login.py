import firebase_admin
from firebase_admin import auth

def email_password_login(email, password):
    if not firebase_admin._apps:
        firebase_admin.initialize_app()
    user = auth.get_user_by_email(email)
    try:
        user = auth.verify_password(password, user.uid)
        return user.uid
    except firebase_admin.auth.UserNotFoundError:
        raise RuntimeError('User not found')
    except firebase_admin.auth.InvalidEmailError:
        raise RuntimeError('Invalid email')
    except firebase_admin.auth.InvalidPasswordError:
        raise RuntimeError('Invalid password')