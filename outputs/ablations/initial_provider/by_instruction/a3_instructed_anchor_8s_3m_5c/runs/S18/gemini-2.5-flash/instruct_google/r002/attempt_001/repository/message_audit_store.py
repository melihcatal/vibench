import os
from google.cloud import firestore
from typing import Dict, Any

def persist_message_record(record: Dict[str, Any]) -> str:
    """Persists processed message records for later lookup using Google Cloud Firestore.

    Args:
        record: A dictionary representing the processed message record.

    Returns:
        The ID of the newly created Firestore document.
    """
    # Project ID is automatically determined from the environment by the client library
    db = firestore.Client()

    collection_name = os.getenv("FIRESTORE_AUDIT_COLLECTION", "message_audits")
    doc_ref = db.collection(collection_name).add(record)

    return doc_ref[1].id
