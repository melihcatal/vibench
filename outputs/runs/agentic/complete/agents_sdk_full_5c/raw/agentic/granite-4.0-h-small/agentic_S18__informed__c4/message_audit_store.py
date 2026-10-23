import os
from google.cloud import firestore
from datetime import datetime
from messaging_models import normalize_message

DB = firestore.Client()  # Uses GOOGLE_APPLICATION_CREDENTIALS env var
AUDIT_COLLECTION = os.getenv('AUDIT_COLLECTION', 'message_audit')


def store_audit_record(message: dict) -> None:
    """Persist a processed message record in Firestore for later lookup.

    The record captures the original payload plus processing metadata.
    """
    if not isinstance(message, dict):
        raise ValueError('Message must be a dict')
    # Normalized copy (ensures valid JSON)
    record = normalize_message(message.copy())
    # Add audit fields
    record['audit_timestamp'] = datetime.now().isoformat()
    record['source_topic'] = os.getenv('AUDIT_SOURCE_TOPIC', 'default-topic')
    # Generate a reasonable document ID (message ID if present)
    doc_id = message.get('message_id') or str(datetime.now().timestamp())
    db_ref = DB.collection(AUDIT_COLLECTION).document(doc_id)
    db_ref.set(record)
    print(f"Stored audit record for message ID {doc_id}")
