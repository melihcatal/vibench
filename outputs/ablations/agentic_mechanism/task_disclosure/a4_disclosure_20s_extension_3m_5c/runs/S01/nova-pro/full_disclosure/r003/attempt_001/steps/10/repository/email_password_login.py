import firebase_admin
from firebase_admin import auth

def sign_in_with_email_and_password(email, password):
    try:
        user = auth.get_user_by_email(email)
        if user:
            user_record = auth.verify_password(password, user.uid)
            id_token = auth.create_custom_token(user.uid)
            return id_token
        else:
            return 'User not found'
    except firebase_admin.auth.UserNotFoundError:
        return 'User not found'
    except firebase_admin.auth.InvalidIdTokenError:
        return 'Invalid credentials'