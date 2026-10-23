import firebase_admin
from firebase_admin import credentials, auth
import os


def initialize_firebase_app():
    if not firebase_admin._apps:
        project_id = os.environ.get("FIREBASE_PROJECT_ID")
        if not project_id:
            raise ValueError("FIREBASE_PROJECT_ID environment variable not set.")

        # Use Application Default Credentials or Service Account for Admin SDK
        # For simplicity, we'll try to use default credentials, which often works in Cloud environments.
        # For local development, ensure GOOGLE_APPLICATION_CREDENTIALS points to a service account key.
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred, {"projectId": project_id})


def get_firebase_auth_client():
    initialize_firebase_app()
    return auth


def get_firebase_web_api_key():
    api_key = os.environ.get("FIREBASE_WEB_API_KEY")
    if not api_key:
        raise ValueError("FIREBASE_WEB_API_KEY environment variable not set.")
    return api_key
