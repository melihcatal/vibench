import firebase_admin
from firebase_admin import auth

def sign_in_with_email_and_password(email, password):
    try:
        user = auth.get_user_by_email(email)
        user_record = auth.verify_password(password, user.uid)
        id_token = auth.create_custom_token(user.uid)
        return id_token
    except firebase_admin.auth.UserNotFoundError:
        raise ValueError('User not found')
    except firebase_admin.auth.InvalidEmailError:
        raise ValueError('Invalid email')
    except firebase_admin.auth.InvalidPasswordError:
        raise ValueError('Invalid password')