from messaging_client import get_firestore_client
from messaging_models import MessageAuditRecord
import json


def persist_message_audit_record(collection_name: str, record: MessageAuditRecord):
    db = get_firestore_client()
    doc_ref = db.collection(collection_name).document(record.message_id)
    doc_ref.set(
        {
            "timestamp": record.timestamp,
            "status": record.status,
            "details": record.details,
        }
    )
    return doc_ref.id


if __name__ == "__main__":
    pass
