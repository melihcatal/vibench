import os
from google.cloud import firestore


def get_firestore_client():
    """Returns a Google Cloud Firestore client."""
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    return firestore.Client()


def get_collection_name():
    """Returns the Firestore collection name from environment variables."""
    return os.environ.get("FIRESTORE_COLLECTION_NAME", "documents")
