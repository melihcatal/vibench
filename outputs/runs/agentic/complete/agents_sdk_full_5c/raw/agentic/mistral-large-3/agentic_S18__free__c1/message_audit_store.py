import os
from typing import Dict, Any
from google.cloud import firestore
from messaging_models import EventResponse

firestore_client = firestore.Client(project=os.getenv("GOOGLE_CLOUD_PROJECT"))

def store_message_audit(message: EventResponse) -> str:
    doc_ref = firestore_client.collection("message_audits").document(message.message_id)
    doc_ref.set({
        "event_id": message.event_id,
        "payload": message.payload,
        "processed_at": firestore.SERVER_TIMESTAMP
    })
    return doc_ref.id