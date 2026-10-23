import os
from google.cloud import firestore
from identity_models import AuditRecord


def persist_audit_record(record: AuditRecord):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ.get("GOOGLE_FIRESTORE_CREDENTIALS_PATH")
    if not os.environ.get("GOOGLE_FIRESTORE_CREDENTIALS_PATH"):
        raise ValueError("Google Cloud Firestore API credentials path must be set as an environment variable (GOOGLE_FIRESTORE_CREDENTIALS_PATH).")

    db = firestore.Client()
    
    # In a real application, you might want to specify a collection name
    # and potentially a document ID.
    doc_ref = db.collection(u'federated_login_audits').document()
    doc_ref.set({
        u'timestamp': record.timestamp,
        u'event_type': record.event_type,
        u'user_id': record.user_id,
        u'details': record.details
    })
