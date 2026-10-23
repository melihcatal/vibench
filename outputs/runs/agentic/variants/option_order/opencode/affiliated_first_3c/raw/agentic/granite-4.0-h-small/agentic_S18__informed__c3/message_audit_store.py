import os
import json
from google.cloud import firestore

# Firestore client configured via GOOGLE_APPLICATION_CREDENTIALS env var
firestore_client = firestore.Client()


def store_audit_record(record: Dict[str, Any]) -> None:
    """Persist a processed message record to Cloud Firestore."""
    # Use a collection named 'message_audit'
    doc_ref = firestore_client.collection("message_audit").document(record.get("id"))
    doc_ref.set(record)


def get_audit_record(message_id: str) -> Dict[str, Any]:
    """Retrieve a stored audit record by its message ID."""
    doc_ref = firestore_client.collection("message_audit").document(message_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    return {}
