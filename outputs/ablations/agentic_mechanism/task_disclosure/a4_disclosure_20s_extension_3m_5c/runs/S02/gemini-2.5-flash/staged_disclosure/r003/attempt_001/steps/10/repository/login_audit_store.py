
from google.cloud import firestore
import os

def persist_audit_record(user_id, login_time, idp_provider):
    """
    Persists a federated-login audit record in Google Cloud Firestore.
    """
    # Initialize Firestore client
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or authenticate using other methods supported by google-cloud-python
    db = firestore.Client()

    # Create a reference to the 'login_audit_records' collection
    doc_ref = db.collection('login_audit_records').document()

    # Data to be stored
    audit_record = {
        'user_id': user_id,
        'login_time': login_time,
        'idp_provider': idp_provider,
        'timestamp': firestore.SERVER_TIMESTAMP
    }

    # Add the document to the collection
    doc_ref.set(audit_record)
    return doc_ref.id

if __name__ == '__main__':
    # Example usage (replace with actual data)
    # For local testing, ensure you have authenticated with Google Cloud
    # e.g., using `gcloud auth application-default login`
    try:
        record_id = persist_audit_record(
            user_id='test-user-123',
            login_time='2026-09-20T10:00:00Z',
            idp_provider='google'
        )
        print(f"Audit record persisted with ID: {record_id}")
    except Exception as e:
        print(f"Error persisting audit record: {e}")
