import os
import firebase_admin
from firebase_admin import credentials, auth


def initialize_firebase():
    if not firebase_admin._apps:
        try:
            # For local development, load from a file specified by GOOGLE_APPLICATION_CREDENTIALS
            # In production, Firebase automatically uses environment variables or service account if deployed on GCP
            cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
            if cred_path and os.path.exists(cred_path):
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
            else:
                # Attempt to initialize using default credentials (e.g., from environment variables on GCP)
                firebase_admin.initialize_app()
            print("Firebase Admin SDK initialized successfully.")
        except Exception as e:
            print(f"Error initializing Firebase Admin SDK: {e}")
            raise


initialize_firebase()
