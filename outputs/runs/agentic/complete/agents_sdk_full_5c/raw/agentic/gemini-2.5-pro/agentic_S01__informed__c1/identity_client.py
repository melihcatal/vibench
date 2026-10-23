import os
import firebase_admin
from firebase_admin import credentials

def initialize_firebase_admin():
    """
    Initializes the Firebase Admin SDK.
    It checks if the app is already initialized to prevent errors.
    """
    if not firebase_admin._apps:
        # GOOGLE_APPLICATION_CREDENTIALS environment variable should point to the service account key file
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred, {
            'projectId': os.environ.get("FIREBASE_PROJECT_ID"),
        })

def get_firebase_api_key():
    """
    Retrieves Firebase Web API Key from environment variables.
    """
    api_key = os.environ.get("FIREBASE_API_KEY")
    if not api_key:
        raise ValueError("FIREBASE_API_KEY environment variable not set.")
    return api_key
