import os
import datetime
from google.cloud import firestore
from messaging_models import AuditRecord

# Google Cloud Firestore provider-specific signal

def persist_audit_record(record: AuditRecord, collection_name: str = "message_audit") -> str:
    # GOOGLE_APPLICATION_CREDENTIALS should be set in the environment for authentication
    db = firestore.Client()

    doc_ref = db.collection(collection_name).document(record.message_id)
    doc_ref.set(record.to_dict())

    return doc_ref.id
