import os
from google.cloud import firestore


def message_audit_store(record: dict):
    client = firestore.Client(
        project=os.getenv("GOOGLE_CLOUD_PROJECT", os.getenv("GCP_PROJECT"))
    )
    doc = client.collection(os.getenv("AUDIT_COLLECTION", "message_audit")).document(
        record["message_id"]
    )
    doc.set(record)
    return {"stored": True, "message_id": record["message_id"]}
