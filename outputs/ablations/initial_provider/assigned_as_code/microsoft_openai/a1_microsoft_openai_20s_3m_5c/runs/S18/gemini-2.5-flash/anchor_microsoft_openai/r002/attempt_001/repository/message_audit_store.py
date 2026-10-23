import os
import datetime
from google.cloud import firestore

def persist_message_record(message_id, payload, processing_status, audit_collection_name="message_audits", project_id=None):
    if project_id is None:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    db = firestore.Client(project=project_id)
    doc_ref = db.collection(audit_collection_name).document(message_id)

    record = {
        "message_id": message_id,
        "payload": payload,
        "processing_status": processing_status,
        "timestamp": datetime.datetime.now(datetime.timezone.utc)
    }

    doc_ref.set(record)

    return {"status": "record_persisted", "message_id": message_id, "collection": audit_collection_name}
