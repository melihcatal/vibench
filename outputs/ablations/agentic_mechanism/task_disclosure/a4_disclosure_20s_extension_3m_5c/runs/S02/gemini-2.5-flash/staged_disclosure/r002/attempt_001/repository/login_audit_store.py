import os
from google.cloud import firestore

def store_audit_record(record: dict):
    """
    Persists a federated-login audit record in Google Cloud Firestore.
    """
    # Initialize Firestore client
    # The client will use the project ID from the GOOGLE_CLOUD_PROJECT environment variable
    # or from the active gcloud configuration.
    db = firestore.Client()

    # Create a reference to the 'login_audit_records' collection
    collection_ref = db.collection('login_audit_records')

    # Add the record to the collection
    collection_ref.add(record)
