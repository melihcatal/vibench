import firebase_admin
from firebase_admin import credentials, auth

# Initialize the Firebase Admin SDK
cred = credentials.Certificate('path/to/serviceAccountKey.json')
firebase_admin.initialize_app(cred)

def sign_in_with_email_and_password(email, password):
    try:
        user = auth.get_user_by_email(email)
        # Check if the user is already signed in
        if user.tokens:
            return user.tokens
        else:
            # Sign in the user with email and password
            user = auth.sign_in_with_email_and_password(email, password)
            return user.tokens
    except Exception as e:
        return str(e)
