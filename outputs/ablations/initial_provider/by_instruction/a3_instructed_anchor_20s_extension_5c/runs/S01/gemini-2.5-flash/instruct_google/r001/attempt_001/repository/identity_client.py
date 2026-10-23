import os
import firebase_admin
from firebase_admin import credentials, auth

# Google Cloud Project ID
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-gcp-project-id")

# Firebase Web API Key for client-side authentication calls
FIREBASE_WEB_API_KEY = os.getenv("FIREBASE_WEB_API_KEY", "your-firebase-web-api-key")

def initialize_firebase_admin():
    """
    Initializes the Firebase Admin SDK if it hasn't been initialized yet.
    Requires a service account key file (e.g., serviceAccountKey.json).
    """
    if not firebase_admin._apps:
        # Path to your Firebase service account key file
        # Ensure this environment variable is set or the file exists at the specified path.
        service_account_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH", "path/to/your/serviceAccountKey.json")
        cred = credentials.Certificate(service_account_path)
        firebase_admin.initialize_app(cred, {'projectId': PROJECT_ID})

