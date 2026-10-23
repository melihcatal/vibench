import os
from google.cloud import firestore
from messaging_models import EventMessage

db = firestore.Client(project=os.getenv("GOOGLE_CLOUD_PROJECT"))

def store_message_audit(event: EventMessage, status: str) -> str:
    doc_ref = db.collection("message_audits").document(event.event_id)
    doc_ref.set({
        "event_id": event.event_id,
        "event_type": event.event_type,
        "payload": event.payload,
        "status": status,
        "timestamp": firestore.SERVER_TIMESTAMP
    })
    return event.event_id