import os
from firebase_admin import auth, credentials

# Initialize the Firebase Admin SDK
cred = credentials.Certificate(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
auth.verify_id_token(cred)

# Sign in a user with email and password
def email_password_login(email, password):
    try:
        user = auth.get_user_by_email(email)
        custom_token = auth.create_custom_token(user.uid)
        return custom_token
    except Exception as e:
        raise e