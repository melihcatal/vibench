import os
from google.cloud import firestore
from messaging_models import AuditRecord
import datetime


def persist_audit_record(record: AuditRecord):
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    db = firestore.Client()
    collection_ref = db.collection("message_audit_records")

    doc_ref = collection_ref.document(record.message_id)
    doc_ref.set(record.to_dict())
    print(f"Audit record for message ID {record.message_id} persisted to Firestore.")


def get_audit_record(message_id: str) -> AuditRecord | None:
    db = firestore.Client()
    collection_ref = db.collection("message_audit_records")
    doc_ref = collection_ref.document(message_id)
    doc = doc_ref.get()

    if doc.exists:
        data = doc.to_dict()
        print(f"Retrieved audit record for message ID {message_id}.")
        return AuditRecord(
            message_id=data["message_id"],
            status=data["status"],
            timestamp=data["timestamp"],
            payload=data["payload"],
            summary=data.get("summary"),
            safety_score=data.get("safety_score"),
            translated_payload=data.get("translated_payload"),
        )
    else:
        print(f"No audit record found for message ID {message_id}.")
        return None
