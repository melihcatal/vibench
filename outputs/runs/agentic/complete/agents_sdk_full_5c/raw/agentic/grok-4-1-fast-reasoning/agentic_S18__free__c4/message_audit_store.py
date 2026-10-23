from google.cloud import firestore
from typing import Dict, Any

def store_message_audit(record: Dict[str, Any]) -> str:
    db = firestore.Client()
    _, doc_ref = db.collection('message_audits').add(record)
    return doc_ref.id