import os
import json
from google.cloud import firestore
from google.cloud.firestore import DocumentReference

# Firestore authentication via env var
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

def init_firestore() -> firestore.Client:
    return firestore.Client()

_audit_db = init_firestore()

AUDIT_COLLECTION = 'message_audit'

def store_audit_record(record: dict) -> DocumentReference:
    """Persist a processed message record to Firestore.","""
    # Ensure record has an ID for later lookup; use record id if present
    doc_id = record.get('msg_id') or record.get('id') or None
    ref: DocumentReference = _audit_db.collection(AUDIT_COLLECTION).document(doc_id)
    ref.set(record)
    print(f"Stored audit record id={doc_id}")
    return ref

if __name__ == '__main__':
    sample_record = {
        'msg_id': 'abc-123',
        'topic': 'my-events',
        'status': 'delivered',
        'timestamp': '2024-08-15T10:30:00Z',
    }
    store_audit_record(sample_record)
