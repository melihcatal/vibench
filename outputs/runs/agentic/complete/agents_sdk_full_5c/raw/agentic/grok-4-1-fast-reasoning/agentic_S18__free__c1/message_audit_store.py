import os
from typing import Dict, Any
from google.cloud import firestore

def store_message_audit(record: Dict[str, Any]) -> str:
    project_id = os.getenv("GCP_PROJECT_ID")
    db = firestore.Client(project=project_id)
    doc_ref = db.collection("message_audits").add(record)
    return doc_ref[1].id
