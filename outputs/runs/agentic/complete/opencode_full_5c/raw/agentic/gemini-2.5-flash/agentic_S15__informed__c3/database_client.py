import os
from google.cloud import firestore


def get_firestore_client():
    # Google Cloud Firestore client
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    return firestore.Client()
