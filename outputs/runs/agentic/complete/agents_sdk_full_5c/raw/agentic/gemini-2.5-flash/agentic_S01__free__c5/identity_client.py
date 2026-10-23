import firebase_admin
from firebase_admin import credentials, auth
import os

def initialize_firebase_admin():
    """
    Initializes the Firebase Admin SDK if not already initialized.
    Expects GOOGLE_APPLICATION_CREDENTIALS environment variable to be set
    to the path of the Firebase service account key file.
    """
    if not firebase_admin._apps:
        try:
            cred = credentials.ApplicationDefault()
            firebase_admin.initialize_app(cred)
            print("Firebase Admin SDK initialized successfully.")
        except Exception as e:
            print(f"Error initializing Firebase Admin SDK: {e}")

def get_firebase_web_api_key() -> str:
    """
    Retrieves the Firebase Web API Key from environment variables.
    This key is used for client-side authentication requests (e.g., sign-in).
    """
    api_key = os.environ.get("FIREBASE_WEB_API_KEY")
    if not api_key:
        print("Warning: FIREBASE_WEB_API_KEY environment variable not set. Some functions may fail.")
    return api_key

# Call initialization on import if desired, or leave for explicit calls.
# initialize_firebase_admin()
