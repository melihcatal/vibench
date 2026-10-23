import os
from google.cloud import firestore

def get_firestore_client():
    # Google Cloud project ID is read from the GOOGLE_CLOUD_PROJECT environment variable
    # or automatically detected when running on Google Cloud services.
    # For local development, ensure GOOGLE_CLOUD_PROJECT is set or provide it explicitly.
    # The client will automatically use Application Default Credentials.
    db = firestore.Client()
    return db
