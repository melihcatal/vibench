import os
from firebase_admin import auth, credentials

# Initialize the Firebase Admin SDK
cred = credentials.Certificate(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
auth.verify_id_token(cred)

# Start a password reset flow for a local account
def password_reset(email):
    try:
        auth.generate_password_reset_link(email)
        return 'Password reset link sent'
    except Exception as e:
        raise e