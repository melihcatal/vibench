import os
from google.cloud import firestore

# Provider configuration
GCLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")

# Initialized Firestore client
DB = firestore.Client(project=GCLOUD_PROJECT) if GCLOUD_PROJECT else None


def store_expense(record: dict):
    """Persist a normalized expense record to Cloud Firestore."""
    if not DB:
        raise RuntimeError("Firestore client not configured")
    # Use a collection named 'expenses'; document ID can be a UUID or receipt name.
    doc_ref = DB.collection('expenses').document()
    doc_ref.set(record)
    return doc_ref.id
