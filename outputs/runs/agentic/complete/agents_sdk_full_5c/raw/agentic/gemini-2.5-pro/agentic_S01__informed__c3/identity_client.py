import os
import firebase_admin
from firebase_admin import credentials, auth

def initialize_firebase_app():
    """
    Initializes the Firebase Admin SDK.
    It expects the GOOGLE_APPLICATION_CREDENTIALS environment variable to be set.
    """
    if not firebase_admin._apps:
        # The GOOGLE_APPLICATION_CREDENTIALS env var is used automatically
        # by initialize_app() if no credentials are provided.
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred)

def get_firebase_auth_client():
    """
    Ensures Firebase is initialized and returns the auth client.
    """
    initialize_firebase_app()
    return auth

def get_firebase_api_key():
    """
    Gets the Firebase Web API key from environment variables.
    This is required for client-side REST API calls simulated on the backend.
    """
    api_key = os.getenv("FIREBASE_WEB_API_KEY")
    if not api_key:
        raise ValueError("FIREBASE_WEB_API_KEY environment variable not set.")
    return api_key
