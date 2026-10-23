import os
from typing import Dict, Any
from google.cloud import firestore

db = firestore.Client(project=os.getenv("GCP_PROJECT_ID"))


def store_processed_message(record: Dict[str, Any]) -> str:
    doc_ref = db.collection("message_audits").add(record)
    return doc_ref[1].id
