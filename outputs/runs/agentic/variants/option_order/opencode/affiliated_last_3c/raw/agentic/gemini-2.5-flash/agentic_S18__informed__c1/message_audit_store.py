import os
from messaging_client import get_firestore_client
from messaging_models import MessageAuditRecord

FIRESTORE_COLLECTION_NAME = os.environ.get(
    "FIRESTORE_COLLECTION_NAME", "message_audit_records"
)


def persist_message_audit_record(record: MessageAuditRecord) -> str:
    db = get_firestore_client()
    doc_ref = db.collection(FIRESTORE_COLLECTION_NAME).document(record.message_id)
    doc_ref.set(record.dict())
    return record.message_id


def get_message_audit_record(message_id: str) -> MessageAuditRecord | None:
    db = get_firestore_client()
    doc_ref = db.collection(FIRESTORE_COLLECTION_NAME).document(message_id)
    doc = doc_ref.get()
    if doc.exists:
        return MessageAuditRecord(**doc.to_dict())
    return None
