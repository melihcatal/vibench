import os
from google.cloud import firestore
from messaging_models import EventMessage

def audit_message(event_id: str, payload: dict, status: str):
    """Persist processed event details to Firestore.",
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    db = firestore.Client()
    doc_ref = db.collection('processed_messages').document(event_id)
    doc_ref.set({
        'payload': payload,
        'status': status,
        'timestamp': firestore.SERVER_TIMESTAMP
    })
    print(f"Audited event {event_id} stored in Firestore.")
