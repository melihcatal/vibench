import firebase_admin
from firebase_admin import auth
from firebase_admin.credentials import Certificate

# Initialize the Firebase Admin SDK with your project's service account key
cred = Certificate('path/to/serviceAccountKey.json')
firebase_admin.initialize_app(cred)

def sign_in_with_email_and_password(email, password):
    try:
        user = auth.get_user_by_email(email)
        # Verify the password
        auth.verify_password(password, user.uid)
        # Create custom tokens
        custom_token = auth.create_custom_token(user.uid)
        return custom_token
    except firebase_admin.auth.UserNotFoundError:
        print('User not found')
        return None
    except firebase_admin.auth.InvalidIdTokenError:
        print('Invalid credentials')
        return None