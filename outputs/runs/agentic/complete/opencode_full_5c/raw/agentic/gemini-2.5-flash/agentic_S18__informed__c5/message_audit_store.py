import os
from google.cloud import firestore
from messaging_models import AuditRecord


def persist_message_record(collection_id: str, record: AuditRecord):
    """Persists processed message records for later lookup using Google Firestore.

    Args:
        collection_id: The ID of the Firestore collection to store the record.
        record: The AuditRecord object to persist.
    """
    db = firestore.Client()

    try:
        doc_ref = db.collection(collection_id).document(record.message_id)
        doc_ref.set(dataclasses.asdict(record))
        print(
            f"Audit record for message ID {record.message_id} persisted to Firestore."
        )
    except Exception as e:
        print(f"Error persisting audit record to Firestore: {e}")
