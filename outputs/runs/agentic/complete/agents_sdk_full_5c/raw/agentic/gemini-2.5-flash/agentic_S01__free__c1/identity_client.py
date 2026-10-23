import os
import firebase_admin
from firebase_admin import credentials

_firebase_app = None

def get_firebase_app():
    global _firebase_app
    if _firebase_app is None:
        # Ensure FIREBASE_SERVICE_ACCOUNT_PATH env var is set to your Firebase service account key file
        service_account_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH", "path/to/your/serviceAccountKey.json")
        cred = credentials.Certificate(service_account_path)
        _firebase_app = firebase_admin.initialize_app(cred)
    return _firebase_app

def get_firebase_api_key():
    # Ensure FIREBASE_WEB_API_KEY env var is set to your Firebase Web API Key
    api_key = os.getenv("FIREBASE_WEB_API_KEY", "YOUR_FIREBASE_WEB_API_KEY")
    if api_key == "YOUR_FIREBASE_WEB_API_KEY":
        raise ValueError("FIREBASE_WEB_API_KEY environment variable not set or is default value.")
    return api_key
