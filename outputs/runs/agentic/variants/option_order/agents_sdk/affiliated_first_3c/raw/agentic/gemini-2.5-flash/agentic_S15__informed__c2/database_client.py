import os
from google.cloud import firestore

def get_firestore_client():
    """Provides a configured Google Cloud Firestore client."""
    # Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or running in a Google Cloud environment.
    client = firestore.Client()
    return client

# Example of how to use it in other files:
# from database_client import get_firestore_client
# db = get_firestore_client()
# doc_ref = db.collection('my_collection').document('my_document')
