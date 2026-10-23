import os
from google.cloud import firestore


def get_firestore_client():
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    # For local development, ensure your gcloud is authenticated:
    # gcloud auth application-default login
    return firestore.Client()


def get_collection_name():
    return os.environ.get("FIRESTORE_COLLECTION_NAME", "documents")
