import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
import os

def initialize_firebase_app():
    if not firebase_admin._apps:
        # Use a service account file from an environment variable, or default to a local file
        service_account_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH", "path/to/your/serviceAccountKey.json")
        try:
            cred = credentials.Certificate(service_account_path)
            firebase_admin.initialize_app(cred)
            print("Firebase Admin SDK initialized successfully.")
        except Exception as e:
            print(f"Error initializing Firebase Admin SDK: {e}")
            raise
    return firebase_admin.get_app()

def get_firebase_auth_client():
    app = initialize_firebase_app()
    return auth
