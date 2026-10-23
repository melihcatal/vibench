import firebase_admin
from firebase_admin import credentials, auth
import os

# Initialize Firebase Admin SDK if not already initialized
if not firebase_admin._apps:
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred)

def register_user(email, password):
    """
    Creates a new email/password user account in Firebase Authentication.
    """
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        return {"uid": user.uid, "email": user.email}
    except Exception as e:
        raise Exception(f"Firebase user registration failed: {e}")
