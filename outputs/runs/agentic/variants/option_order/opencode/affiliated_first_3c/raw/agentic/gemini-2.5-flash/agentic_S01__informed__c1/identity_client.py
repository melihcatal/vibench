import firebase_admin
from firebase_admin import credentials
import os


# Initialize Firebase Admin SDK if not already initialized
def get_firebase_app():
    if not firebase_admin._apps:
        try:
            # Path to your service account key file
            # For Google Cloud environments, GOOGLE_APPLICATION_CREDENTIALS might be set,
            # or it can pick up credentials automatically.
            # For local development, ensure FIREBASE_SERVICE_ACCOUNT_KEY env var points to the JSON file path.
            service_account_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
            if not service_account_path:
                raise ValueError(
                    "GOOGLE_APPLICATION_CREDENTIALS environment variable not set."
                )

            cred = credentials.Certificate(service_account_path)
            firebase_admin.initialize_app(cred)
            print("Firebase Admin SDK initialized successfully.")
        except Exception as e:
            print(f"Error initializing Firebase Admin SDK: {e}")
            raise
    return firebase_admin.get_app()
