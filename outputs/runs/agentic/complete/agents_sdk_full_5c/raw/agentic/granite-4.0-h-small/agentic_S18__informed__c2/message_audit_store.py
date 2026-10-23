import os
import json
from google.cloud import firestore
from messaging_models import PubSubMessage, ProcessingResult

def audit_message(message: PubSubMessage, result: ProcessingResult) -> None:
    """Persist a processed message record to Cloud Firestore.

    The document ID will be the Pub/Sub message ID.
    """
    db = firestore.Client()  # Uses GOOGLE_APPLICATION_CREDENTIALS env var
    collection = db.collection("processed_messages")
    doc_ref = collection.document(message.message_id)
    doc_ref.set(result)
    print(f"Audited message {message.message_id} in Firestore:", result)

if __name__ == "__main__":
    # Demo (requires GOOGLE_APPLICATION_CREDENTIALS env var set)
    demo_payload = {"event_id": "audit-demo", "body": "sample audit"}
    msg = PubSubMessage(data=json.dumps(demo_payload).encode())
    audit_message(msg, build_processing_result(msg.message_id, "ok"))
