import firebase_admin
from firebase_admin import credentials, auth

def initialize_app():
    cred = credentials.Certificate('path/to/serviceAccountKey.json')
    firebase_admin.initialize_app(cred)

def get_onboarding_summary(user_id):
    user = auth.get_user(user_id)
    summary = {
        'user_id': user.uid,
        'email': user.email,
        'email_verified': user.email_verified,
        'created_at': user.created_at,
        'last_login_at': user.last_login_at,
        'disabled': user.disabled,
    }
    return summary