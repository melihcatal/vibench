# identity_client.py
import os
import firebase_admin
from firebase_admin import credentials, auth

def initialize_firebase_admin():
    """
    Initializes the Firebase Admin SDK.
    It checks if the app is already initialized to prevent errors.
    """
    if not firebase_admin._apps:
        # GOOGLE_APPLICATION_CREDENTIALS environment variable
        # should be set to the path of the service account key file.
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred, {
            'projectId': os.getenv("FIREBASE_PROJECT_ID"),
        })
    return auth

def get_firebase_web_api_key():
    """
    Returns the Firebase Web API Key for client-side REST API calls.
    """
    api_key = os.getenv("FIREBASE_WEB_API_KEY")
    if not api_key:
        raise ValueError("FIREBASE_WEB_API_KEY environment variable not set.")
    return api_key
