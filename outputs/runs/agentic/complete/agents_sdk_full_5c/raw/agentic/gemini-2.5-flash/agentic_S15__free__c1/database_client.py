from google.cloud import firestore
import os

def get_firestore_client():
    """Provides a configured Firestore client."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    return firestore.Client(project=project_id)

def get_collection_ref(collection_name: str):
    """Provides a reference to a Firestore collection."""
    db = get_firestore_client()
    return db.collection(collection_name)
