import os
from google.cloud import firestore


def get_firestore_client():
    """Initializes and returns a Google Firestore client."""
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    # to the path of your service account key file.
    return firestore.Client()
