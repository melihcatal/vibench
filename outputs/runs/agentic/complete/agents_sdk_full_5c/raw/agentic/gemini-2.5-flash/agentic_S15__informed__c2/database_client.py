import os
from google.cloud import firestore

def get_firestore_client():
    """Initializes and returns a Firestore client."""
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    # for authentication.
    return firestore.Client()

def get_database_id():
    """Returns the Firestore database ID (project ID)."""
    # In Firestore, the project ID is typically used as the database identifier.
    return os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
