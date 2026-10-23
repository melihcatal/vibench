import os
import datetime
from google.cloud import firestore

def persist_audit_record(user_id: str, event_type: str, details: dict):
    db = firestore.Client()
    
    audit_ref = db.collection("audit_logs").document()
    
    record = {
        "user_id": user_id,
        "event_type": event_type,
        "details": details,
        "timestamp": datetime.datetime.now(datetime.timezone.utc)
    }
    
    audit_ref.set(record)
