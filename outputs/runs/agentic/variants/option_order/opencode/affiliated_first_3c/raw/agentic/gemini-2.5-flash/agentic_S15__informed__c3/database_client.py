import os
from google.cloud import firestore


def get_firestore_client():
    """Returns a Google Firestore client."""
    return firestore.Client()
