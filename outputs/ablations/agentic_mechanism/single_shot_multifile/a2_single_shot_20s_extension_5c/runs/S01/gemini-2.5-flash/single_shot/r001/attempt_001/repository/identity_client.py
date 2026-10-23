import os
import firebase_admin
from firebase_admin import credentials

_firebase_app = None

def get_firebase_app():
    global _firebase_app
    if _firebase_app is None:
        firebase_project_id = os.environ.get("FIREBASE_PROJECT_ID")
        if not firebase_project_id:
            raise EnvironmentError("FIREBASE_PROJECT_ID environment variable not set.")

        # Initialize Firebase Admin SDK using GOOGLE_APPLICATION_CREDENTIALS or default project ID
        # For local development, ensure `gcloud auth application-default login` is run
        # or `GOOGLE_APPLICATION_CREDENTIALS` points to a service account key file.
        try:
            _firebase_app = firebase_admin.initialize_app(
                credentials.ApplicationDefault(), 
                options={'projectId': firebase_project_id}
            )
        except ValueError:
            # If app is already initialized in a different context (e.g., test suite)
            _firebase_app = firebase_admin.get_app()

    return _firebase_app