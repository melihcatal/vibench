import os
import firebase_admin
from firebase_admin import credentials

def initialize_firebase_admin():
    """Initializes the Firebase Admin SDK if not already initialized."""
    if not firebase_admin._apps:
        try:
            # Ensure the path to your service account key file is set in environment variables
            service_account_key_path = os.environ.get("FIREBASE_SERVICE_ACCOUNT_KEY_PATH")
            if not service_account_key_path or not os.path.exists(service_account_key_path):
                raise ValueError("FIREBASE_SERVICE_ACCOUNT_KEY_PATH environment variable not set or file not found.")
            cred = credentials.Certificate(service_account_key_path)
            firebase_admin.initialize_app(cred)
            print("Firebase Admin SDK initialized successfully.")
        except Exception as e:
            print(f"Error initializing Firebase Admin SDK: {e}")
            raise

