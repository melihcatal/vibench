from typing import Dict, Any
from google.cloud import firestore

db = firestore.Client()


def store_processed_message(record: Dict[str, Any]) -> str:
    _, doc_ref = db.collection("message_audits").add(record)
    return doc_ref.id
