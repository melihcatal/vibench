import firebase_admin
from firebase_admin import credentials, auth

def sign_in_with_email_and_password(email, password):
    if not firebase_admin._apps:
        cred = credentials.Certificate('path/to/serviceAccountKey.json')
        firebase_admin.initialize_app(cred)
    try:
        user = auth.get_user_by_email(email)
        custom_token = auth.create_custom_token(user.uid)
        return custom_token
    except firebase_admin.auth.UserNotFoundError:
        raise Exception('User not found')
    except firebase_admin.auth.InvalidIdTokenError:
        raise Exception('Invalid credentials')