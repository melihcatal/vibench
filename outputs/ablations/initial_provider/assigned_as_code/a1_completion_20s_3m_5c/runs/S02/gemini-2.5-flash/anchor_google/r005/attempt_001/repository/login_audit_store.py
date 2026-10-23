import os
import datetime
from google.cloud import firestore
from identity_models import AuditRecord

def store_audit_record(record: AuditRecord):
    project_id = os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID must be set in environment variables")

    db = firestore.Client(project=project_id)
    
    # Add a new doc in collection 'audit_logs' with ID 'record.user_id_timestamp'
    doc_ref = db.collection("audit_logs").document(f"{record.user_id}_{datetime.datetime.now().isoformat()}")
    doc_ref.set({
        "event_type": record.event_type,
        "timestamp": record.timestamp,
        "user_id": record.user_id,
        "details": record.details,
    })

def get_audit_records(user_id: str = None, event_type: str = None, limit: int = 10) -> list[AuditRecord]:
    project_id = os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID must be set in environment variables")

    db = firestore.Client(project=project_id)
    
    query = db.collection("audit_logs").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(limit)

    if user_id:
        query = query.where("user_id", "==", user_id)
    if event_type:
        query = query.where("event_type", "==", event_type)
        
    results = query.stream()
    
    records = []
    for doc in results:
        data = doc.to_dict()
        records.append(AuditRecord(
            event_type=data.get("event_type"),
            timestamp=data.get("timestamp"),
            user_id=data.get("user_id"),
            details=data.get("details", {})
        ))
    return records
