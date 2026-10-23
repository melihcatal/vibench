import os
import datetime
from google.cloud import firestore
from messaging_models import MessageAuditRecord

def persist_message_audit_record(record: MessageAuditRecord, collection_name: str = "message_audits") -> str:
    project_id = os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable not set.")

    db = firestore.Client(project=project_id)
    
    # Add a server timestamp for consistency
    record['timestamp'] = datetime.datetime.now(datetime.timezone.utc).isoformat()

    doc_ref = db.collection(collection_name).document()
    doc_ref.set(record)

    return doc_ref.id
