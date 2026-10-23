from google.cloud import firestore
from messaging_models import AuditRecord
import os

def store_audit_record(record: AuditRecord):
    # Provider: Google Firestore
    # Auth: GOOGLE_APPLICATION_CREDENTIALS
    db = firestore.Client()

    # Create a new document in a collection called 'message_audits'
    doc_ref = db.collection("message_audits").document(record.message_id)
    doc_ref.set(record.model_dump())
    print(f"Audit record for message {record.message_id} stored in Firestore.")
