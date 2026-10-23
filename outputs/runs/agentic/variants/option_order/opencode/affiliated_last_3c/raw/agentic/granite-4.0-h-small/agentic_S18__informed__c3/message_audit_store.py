import os
from typing import Dict, Any
import google.cloud.firestore_v1 as firestore


def store_audit_record(message: Dict[str, Any]) -> None:
    """Persist a processed Pub/Sub message record to Firestore.

    Firestore collection \"processed_messages\" will hold a document per event.
    """
    db = firestore.Client()  # picks up credentials from GOOGLE_APPLICATION_CREDENTIALS
    collection = db.collection("processed_messages")
    doc_id = message.get("event_id") or str(firestore.gen_uid())
    doc_ref = collection.document(doc_id)
    doc_ref.set(message)
    print(f"Stored audit record for event {doc_id}")
