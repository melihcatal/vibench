import os
import datetime
from google.cloud import firestore
from identity_models import AuditRecord

def get_firestore_client():
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set for Firestore.")
    return firestore.Client(project=project_id)

def persist_audit_record(audit_record: AuditRecord):
    db = get_firestore_client()
    
    collection_name = "federated_login_audits"
    audit_data = audit_record.to_dict()
    
    if not isinstance(audit_data.get("timestamp"), datetime.datetime):
        try:
            audit_data["timestamp"] = datetime.datetime.fromisoformat(audit_data["timestamp"])
        except (ValueError, KeyError):
            audit_data["timestamp"] = datetime.datetime.utcnow()

    try:
        doc_ref = db.collection(collection_name).add(audit_data)
        return doc_ref[1].id
    except Exception as e:
        raise RuntimeError(f"Failed to persist audit record to Google Cloud Firestore: {e}")