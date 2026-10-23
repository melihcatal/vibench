import os
import firebase_admin
from firebase_admin import credentials

def initialize_firebase_app():
    """Initializes the Firebase Admin SDK if not already initialized."""
    # This assumes GOOGLE_APPLICATION_CREDENTIALS or GOOGLE_CLOUD_PROJECT
    # environment variables are set for authentication.
    if not firebase_admin._apps:
        try:
            cred = credentials.ApplicationDefault()
            firebase_admin.initialize_app(cred)
            print("Firebase Admin SDK initialized successfully.")
        except Exception as e:
            print(f"Error initializing Firebase Admin SDK: {e}")
            raise

def get_firebase_web_api_key() -> str:
    """Retrieves the Firebase Web API Key from environment variables."""
    api_key = os.environ.get("FIREBASE_WEB_API_KEY")
    if not api_key:
        raise ValueError("FIREBASE_WEB_API_KEY environment variable not set.")
    return api_key
