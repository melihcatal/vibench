import os
from google.cloud import firestore
from typing import Dict
from datetime import datetime

client = firestore.Client()
COLLECTION_NAME = os.getenv("FIRESTORE_COLLECTION_NAME", "message_audits")

def store_message_audit(event_id: str, payload: Dict, status: str) -> str:
    doc_ref = client.collection(COLLECTION_NAME).document(event_id)
    
    doc_ref.set({
        "event_id": event_id,
        "payload": payload,
        "status": status,
        "timestamp": datetime.utcnow()
    })
    
    return doc_ref.id