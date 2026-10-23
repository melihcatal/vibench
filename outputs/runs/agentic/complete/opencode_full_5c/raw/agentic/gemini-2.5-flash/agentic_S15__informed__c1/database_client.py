from google.cloud import firestore
import os


def get_firestore_client():
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # For local development, you might set it like:
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    return firestore.Client()
