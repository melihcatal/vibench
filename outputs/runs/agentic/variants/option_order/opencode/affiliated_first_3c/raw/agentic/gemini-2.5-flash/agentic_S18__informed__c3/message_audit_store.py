from google.cloud import firestore
import os
import datetime
from messaging_models import AuditRecord


def persist_audit_record(record: AuditRecord) -> str:
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    db = firestore.Client()

    collection_ref = db.collection("message_audit_records")

    record_dict = {
        "message_id": record.message_id,
        "event_type": record.event_type,
        "timestamp": record.timestamp,
        "payload_snapshot": record.payload_snapshot,
        "processing_status": record.processing_status,
    }

    if record.record_id:
        doc_ref = collection_ref.document(record.record_id)
        doc_ref.set(record_dict)
        return record.record_id
    else:
        doc_ref = collection_ref.add(record_dict)
        return doc_ref[1].id
