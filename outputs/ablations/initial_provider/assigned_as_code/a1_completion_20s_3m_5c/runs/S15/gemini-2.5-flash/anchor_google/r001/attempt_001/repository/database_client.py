from google.cloud import firestore
import os


def get_firestore_client():
    project_id = os.environ.get("FIRESTORE_PROJECT_ID")
    if not project_id:
        raise ValueError("FIRESTORE_PROJECT_ID environment variable not set.")
    return firestore.Client(project=project_id)
