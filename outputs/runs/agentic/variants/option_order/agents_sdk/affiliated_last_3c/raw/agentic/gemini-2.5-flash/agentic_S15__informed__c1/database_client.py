import os
from google.cloud import firestore

def get_firestore_client():
    """Provides a configured Firestore client.
    Assumes GOOGLE_APPLICATION_CREDENTIALS or default project is set up.
    """
    # For local development with emulator, set FIRESTORE_EMULATOR_HOST environment variable.
    # e.g., os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
    return firestore.Client()
