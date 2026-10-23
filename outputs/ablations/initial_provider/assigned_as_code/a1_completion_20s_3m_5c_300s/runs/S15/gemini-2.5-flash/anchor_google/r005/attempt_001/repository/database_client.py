from google.cloud import firestore
import os


def get_firestore_client(project_id: str = None):
    project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("Google Cloud Project ID not provided and not found in GOOGLE_CLOUD_PROJECT environment variable.")
    return firestore.Client(project=project_id)
