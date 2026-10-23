import firebase_admin
from firebase_admin import credentials, auth
import os

# Initialize Firebase Admin SDK if not already initialized
if not firebase_admin._apps:
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred)

def password_reset(email):
    """
    Starts a password reset flow for a Firebase account by sending a reset email.
    """
    try:
        link = auth.generate_password_reset_link(email)
        return {"email": email, "message": f"Password reset link generated for {email}. Link: {link}"}
    except auth.UserNotFoundError:
        raise Exception(f"No user found with email: {email}")
    except Exception as e:
        raise Exception(f"Failed to start password reset for {email}: {e}")
