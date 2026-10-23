import os
from google.cloud import firestore

from identity_models import AuditRecord

# GOOGLE_APPLICATION_CREDENTIALS should be set in the environment

def store_audit_record(record: AuditRecord, collection_name: str = "login_audit_records"): -> str
    """Persists a federated-login audit record in Google Firestore.

    Args:
        record: The AuditRecord object to store.
        collection_name: The name of the Firestore collection to store records in.

    Returns:
        The ID of the created document.

    Raises:
        Exception: If storing the record fails.
    """
    db = firestore.Client()
    doc_ref = db.collection(collection_name).document(record.event_id)

    doc_ref.set({
        "event_id": record.event_id,
        "timestamp": record.timestamp,
        "event_type": record.event_type,
        "user_id": record.user_id,
        "ip_address": record.ip_address,
        "details": record.details,
    })

    return doc_ref.id
