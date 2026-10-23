import os
import firebase_admin
from firebase_admin import credentials, auth


def initialize_firebase():
    if not firebase_admin._apps:
        # Assumes FIREBASE_CREDENTIALS env var points to the service account key file path
        # Or, if running on Google Cloud, it can pick up credentials automatically.
        try:
            cred = credentials.Certificate(
                os.environ.get(
                    "FIREBASE_CREDENTIALS", "path/to/your/serviceAccountKey.json"
                )
            )
            firebase_admin.initialize_app(cred)
        except Exception as e:
            print(
                f"Error initializing Firebase: {e}. Please ensure FIREBASE_CREDENTIALS is set correctly."
            )
            # For demonstration, we'll initialize without a path if env var is missing/invalid
            # In a real app, this should be handled more robustly.
            firebase_admin.initialize_app()
    return firebase_admin.get_app()


def get_firebase_auth():
    initialize_firebase()
    return auth
