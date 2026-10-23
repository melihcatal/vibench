import firebase_admin
from firebase_admin import auth
from firebase_admin.exceptions import FirebaseError

def sign_in_with_email_and_password(email, password):
    try:
        user = auth.get_user_by_email(email)
        if user:
            user = auth.verify_password(password, user.uid)
            custom_token = auth.create_custom_token(user.uid)
            return custom_token
        else:
            return 'User not found'
    except FirebaseError as e:
        return str(e)

# Initialize the Firebase Admin SDK
firebase_admin.initialize_app()