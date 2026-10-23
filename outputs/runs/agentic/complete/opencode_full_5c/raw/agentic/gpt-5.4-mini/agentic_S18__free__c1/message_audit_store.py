import os

from google.cloud import firestore


def message_audit_store(record: dict) -> str:
    client = firestore.Client(project=os.getenv("GOOGLE_CLOUD_PROJECT"))
    doc = client.collection("message_audit").document()
    doc.set(record)
    return doc.id
