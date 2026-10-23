import os
import firebase_admin
from firebase_admin import credentials, auth

def initialize_firebase_admin():
    if not firebase_admin._apps:
        # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for service account key path
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred)
    return auth

def get_firebase_web_api_key():
    # This key is typically used for client-side Firebase operations.
    # For server-side interactions requiring it (e.g., REST API calls for email/password login),
    # it must be securely managed.
    api_key = os.getenv("FIREBASE_WEB_API_KEY")
    if not api_key:
        raise ValueError("FIREBASE_WEB_API_KEY environment variable not set.")
    return api_key
