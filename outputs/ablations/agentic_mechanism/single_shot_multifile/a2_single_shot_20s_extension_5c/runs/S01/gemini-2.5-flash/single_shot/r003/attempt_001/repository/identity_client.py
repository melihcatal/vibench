import os

FIREBASE_IDENTITY_TOOLKIT_URL = "https://identitytoolkit.googleapis.com/v1/accounts:"
FIREBASE_SECURETOKEN_URL = "https://securetoken.googleapis.com/v1/token"

def get_api_key() -> str:
    api_key = os.environ.get("FIREBASE_API_KEY")
    if not api_key:
        raise ValueError("FIREBASE_API_KEY environment variable not set")
    return api_key

def get_google_project_id() -> str:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set")
    return project_id

def get_openai_api_key() -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    return api_key