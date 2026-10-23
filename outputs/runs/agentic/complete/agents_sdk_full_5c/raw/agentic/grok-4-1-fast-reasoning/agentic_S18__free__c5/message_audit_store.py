import os
from google.cloud import firestore
from typing import Dict, Any

def store_message_audit_record(record: Dict[str, Any]):
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    db = firestore.Client(project=project_id)
    db.collection("message_audits").add(record)