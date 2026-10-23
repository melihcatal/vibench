import firebase_admin
from firebase_admin import auth

# Initialize the Firebase Admin SDK
firebase_admin.initialize_app()

def sign_in_with_email_and_password(email, password):
    try:
        user = auth.get_user_by_email(email)
        user_record = auth.verify_password(password, user.uid)
        tokens = auth.create_custom_token(user.uid)
        return tokens
    except Exception as e:
        return str(e)