import os

FIREBASE_IDENTITY_TOOLKIT_URL = "https://identitytoolkit.googleapis.com/v1/accounts"

def get_firebase_api_key() -> str:
    api_key = os.getenv("FIREBASE_API_KEY")
    if not api_key:
        raise ValueError("FIREBASE_API_KEY environment variable not set")
    return api_key

def get_google_project_id() -> str:
    project_id = os.getenv("GOOGLE_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_PROJECT_ID environment variable not set")
    return project_id
