import os
from google.cloud import firestore
from datetime import datetime
from typing import Dict

client = firestore.Client(project=os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id"))
COLLECTION_NAME = "processed_messages"

def store_message_audit(message_id: str, metadata: Dict) -> str:
    doc_ref = client.collection(COLLECTION_NAME).document(message_id)
    
    audit_data = {
        **metadata,
        "processed_at": datetime.utcnow(),
        "message_id": message_id
    }
    
    doc_ref.set(audit_data)
    return doc_ref.id