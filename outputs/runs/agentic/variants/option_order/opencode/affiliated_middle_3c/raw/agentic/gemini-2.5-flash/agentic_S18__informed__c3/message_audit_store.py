import os
import datetime
from google.cloud import firestore


def store_message_record(record_data: dict) -> str:
    db = firestore.Client()
    collection_name = os.getenv("FIRESTORE_AUDIT_COLLECTION", "message_audits")
    doc_ref = db.collection(collection_name).document()

    # Add a timestamp to the record
    record_data["timestamp"] = datetime.datetime.now(tz=datetime.timezone.utc)

    doc_ref.set(record_data)
    return doc_ref.id
