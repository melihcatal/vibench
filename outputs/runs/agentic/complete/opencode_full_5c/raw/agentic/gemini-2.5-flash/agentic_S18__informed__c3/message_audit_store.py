from google.cloud import firestore
import os
from datetime import datetime


def persist_message_record(message_id: str, payload: dict, processing_results: dict):
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    db = firestore.Client()

    doc_ref = db.collection("message_audits").document(message_id)
    doc_ref.set(
        {
            "message_id": message_id,
            "payload": payload,
            "processing_results": processing_results,
            "timestamp": datetime.utcnow(),
        }
    )
    return doc_ref.id


def get_message_record(message_id: str):
    db = firestore.Client()
    doc_ref = db.collection("message_audits").document(message_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        return None
