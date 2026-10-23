import os
from typing import List, TypedDict
from google.cloud import firestore
from messaging_models import ConsumeResponse, DeadLetterRequest

DB = firestore.Client()
MESSAGES_COLLECTION = "processed_messages"


class AuditRecord(TypedDict):
    topic: str
    message_id: str
    payload: dict
    timestamp: str
    status: str  # processed, failed, dead_lettered


def store_audit(record: AuditRecord) -> None:
    """Persist a processed message record to Google Cloud Firestore."""
    doc_ref = DB.collection(MESSAGES_COLLECTION).document()
    doc_ref.set(record)
    print(f"Stored audit record {doc_ref.id}")


def retrieve_audit(message_id: str) -> List[AuditRecord]:
    """Fetch all audit records matching a message_id."""
    query = DB.collection(MESSAGES_COLLECTION).where("message_id", "==", message_id)
    docs = query.stream()
    return [doc.to_dict() for doc in docs]


# Example usage within the processing flow (not part of the file):
# store_audit({"topic":"orders", "message_id":msg_id, "payload":msg_body, "timestamp":now, "status":"processed"})
