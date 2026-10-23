import firebase_admin
from firebase_admin import credentials, auth
import os


def get_firebase_app():
    try:
        return firebase_admin.get_app()
    except ValueError:
        # Initialize Firebase Admin SDK if not already initialized
        # For local development, consider setting GOOGLE_APPLICATION_CREDENTIALS environment variable
        # to the path of your service account key file.
        # Alternatively, you can pass the path directly to credentials.Certificate.
        # project_id should also be configured, e.g., via FIREBASE_PROJECT_ID env var.
        cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        project_id = os.getenv("FIREBASE_PROJECT_ID")

        if not cred_path or not project_id:
            raise RuntimeError(
                "Firebase credentials path or project ID not configured.\n" +
                "Please set GOOGLE_APPLICATION_CREDENTIALS and FIREBASE_PROJECT_ID " +
                "environment variables or provide them in a config object."
            )

        cred = credentials.Certificate(cred_path)
        return firebase_admin.initialize_app(cred, options={"projectId": project_id})


def get_auth_client():
    app = get_firebase_app()
    return auth
