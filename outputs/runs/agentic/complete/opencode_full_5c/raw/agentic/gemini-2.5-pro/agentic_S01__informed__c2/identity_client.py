import os
import firebase_admin
from firebase_admin import credentials, auth


def get_firebase_app():
    if not firebase_admin._apps:
        # GOOGLE_APPLICATION_CREDENTIALS environment variable is used automatically
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(
            cred,
            {
                "projectId": os.environ.get("FIREBASE_PROJECT_ID"),
            },
        )
    return firebase_admin.get_app()


def get_auth_client():
    get_firebase_app()
    return auth


def get_firebase_web_api_key():
    api_key = os.environ.get("FIREBASE_WEB_API_KEY")
    if not api_key:
        raise ValueError("FIREBASE_WEB_API_KEY environment variable not set.")
    return api_key
