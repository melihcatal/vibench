import os
from google.cloud import firestore
import datetime

def store_audit_record(record: dict):
    """Persist processed message record to Firestore (managed NoSQL document store)."""
    # Firestore credentials are handled by GOOGLE_APPLICATION_CREDENTIALS env var
    db = firestore.Client()
    doc_ref = db.collection('pubsub_audits').document()
    audited = {
        'message_id': record.get('message_id'),
        'event_payload': record.get('payload', {}),
        'processed_at': datetime.datetime.utcnow().isoformat() + 'Z'
    }
    doc_ref.set(audited)
    print(f"Stored audit record {record.get('message_id')} in Firestore")
