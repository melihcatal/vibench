from google.cloud import firestore
import os


def get_db_client():
    """Initializes and returns a Firestore client."""
    # Ensure GOOGLE_CLOUD_PROJECT environment variable is set for project ID
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    return firestore.Client(project=project_id)
