import firebase_admin
from firebase_admin import auth

def sign_in_with_email_and_password(email, password):
    if not firebase_admin._apps:
        firebase_admin.initialize_app()
    try:
        user = auth.get_user_by_email(email)
        tokens = auth.create_custom_token(user.uid)
        return tokens
    except firebase_admin.auth.UserNotFoundError:
        return 'User not found'
    except firebase_admin.auth.InvalidEmailError:
        return 'Invalid email'
    except firebase_admin.auth.EmailAlreadyExistsError:
        return 'Email already exists'