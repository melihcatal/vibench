import firebase_admin
from firebase_admin import credentials
import os

def initialize_firebase_admin():
    """
    Initializes the Firebase Admin SDK.
    Looks for GOOGLE_APPLICATION_CREDENTIALS environment variable.
    """
    if not firebase_admin._apps:
        try:
            cred = credentials.ApplicationDefault()
            firebase_admin.initialize_app(cred)
            print("Firebase Admin SDK initialized successfully.")
        except Exception as e:
            print(f"Error initializing Firebase Admin SDK: {e}")
            raise

def get_firebase_web_api_key() -> str:
    """
    Retrieves the Firebase Web API Key from environment variables.
    """
    api_key = os.getenv("FIREBASE_WEB_API_KEY")
    if not api_key:
        raise ValueError("FIREBASE_WEB_API_KEY environment variable not set.")
    return api_key

# Ensure Firebase Admin SDK is initialized when this module is imported
# This is a common pattern for helper modules.
initialize_firebase_admin()
