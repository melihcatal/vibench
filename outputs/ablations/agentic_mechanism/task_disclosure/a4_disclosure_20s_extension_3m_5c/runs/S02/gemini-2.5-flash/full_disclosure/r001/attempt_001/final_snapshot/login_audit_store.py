from google.cloud import firestore
import os

def get_firestore_client():
    """Initializes and returns a Google Cloud Firestore client."""
    # The project ID is typically inferred from the environment
    # or explicitly set using GOOGLE_CLOUD_PROJECT environment variable.
    # For local development, ensure GOOGLE_APPLICATION_CREDENTIALS points to your service account key.
    # Replace 'your-gcp-project-id' with your actual Google Cloud Project ID if not using environment variable.
    # client = firestore.Client(project=os.getenv('GOOGLE_CLOUD_PROJECT', 'your-gcp-project-id'))
    client = firestore.Client()
    return client

def persist_audit_record(record: dict):
    """
    Persists a federated-login audit record to Google Cloud Firestore.

    Args:
        record: A dictionary containing the audit record data.
                Example: {
                    "event_type": "login_success",
                    "user_id": "user123",
                    "timestamp": firestore.SERVER_TIMESTAMP,
                    "idp": "google",
                    "details": {"ip_address": "192.168.1.1"}
                }
    """
    db = get_firestore_client()
    # Using a collection named 'federated_login_audit' for audit records
    doc_ref = db.collection('federated_login_audit').document()
    doc_ref.set(record)
    return doc_ref.id
