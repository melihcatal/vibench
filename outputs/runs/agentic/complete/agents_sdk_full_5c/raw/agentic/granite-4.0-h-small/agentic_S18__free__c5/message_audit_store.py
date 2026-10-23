import os
import json
from google.cloud import firestore
from messaging_models import EventMessage

def audit_message(message: dict, status: str):
    """Persist a processed message record to Firestore for audit purposes.
    Args:
        message (dict): Original message payload with fields: event_id, payload, metadata.
        status (str): Processing outcome ('success', 'dead_letter', 'error').
    """
    # Firestore client (application default credentials expected)
    db = firestore.Client()
    collection = db.collection('processed_messages')
    doc_id = message.get('event_id') or str(message.get('message_id', ''))
    # Normalize data for storage
    audit_record = {
        'event_id': message.get('event_id'),
        'payload': message.get('payload'),
        'metadata': message.get('metadata', {}),
        'processed_at': firestore.SERVER_TIMESTAMP,
        'status': status,
    }
    collection.document(doc_id).set(audit_record)
    print(f'Audited message {doc_id} with status {status}')
