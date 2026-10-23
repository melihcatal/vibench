import os
from typing import Dict, Any
from datetime import datetime
from messaging_client import get_firestore_client
from messaging_models import AuditRecord

def persist_message_record(record: AuditRecord, collection_name: str = "message_audits") -> str:
    """Persists processed message records to Google Cloud Firestore for later lookup."""
    client = get_firestore_client()
    
    # Ensure the timestamp is in a Firestore-compatible format if not already
    if isinstance(record.timestamp, str):
        try:
            # Attempt to parse ISO format and convert to datetime object
            record.timestamp = datetime.fromisoformat(record.timestamp.replace('Z', '+00:00'))
        except ValueError:
            # If parsing fails, just use the string, Firestore handles strings too
            pass 

    # Convert dataclass to a dictionary for Firestore
    record_dict = record.__dict__
    # Remove 'record_id' from the dict if we want Firestore to generate one,
    # or use it as the document ID.
    doc_id = record_dict.pop('record_id', None)

    collection_ref = client.collection(collection_name)

    if doc_id:
        doc_ref = collection_ref.document(doc_id)
        doc_ref.set(record_dict)
    else:
        doc_ref = collection_ref.add(record_dict)[1] # add() returns (datetime, DocumentReference)

    return doc_ref.id

def get_message_record(record_id: str, collection_name: str = "message_audits") -> Dict[str, Any]:
    """Retrieves a processed message record from Google Cloud Firestore."""
    client = get_firestore_client()
    doc_ref = client.collection(collection_name).document(record_id)
    doc = doc_ref.get()

    if doc.exists:
        return doc.to_dict()
    else:
        return {}
