import firebase_admin
from firebase_admin import credentials, auth

def sign_in_with_email_and_password(email, password):
    try:
        user = auth.get_user_by_email(email)
        user_record = auth.verify_password(password, user.uid)
        tokens = auth.create_custom_token(user_record.uid)
        return tokens
    except Exception as e:
        print(f"Error signing in: {e}")
        return None

# Initialize the app with a service account, granting admin privileges
cred = credentials.Certificate('path/to/serviceAccountKey.json')
firebase_admin.initialize_app(cred)