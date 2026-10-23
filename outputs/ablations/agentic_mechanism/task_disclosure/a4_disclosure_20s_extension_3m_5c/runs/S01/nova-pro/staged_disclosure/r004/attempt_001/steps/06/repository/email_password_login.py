import firebase_admin
from firebase_admin import credentials, auth

# Initialize the Firebase app
cred = credentials.Certificate('path/to/serviceAccountKey.json')
firebase_admin.initialize_app(cred)

def sign_in_with_email_and_password(email, password):
    try:
        user = auth.get_user_by_email(email)
        user = auth.sign_in_with_email_and_password(email, password)
        return user.id_token, user.refresh_token
    except Exception as e:
        return str(e)
