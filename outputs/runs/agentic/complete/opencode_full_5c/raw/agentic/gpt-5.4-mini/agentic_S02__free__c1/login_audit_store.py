import os

from google.cloud import firestore


def login_audit_store(record: dict) -> dict:
    client = firestore.Client(project=os.environ.get("GOOGLE_CLOUD_PROJECT"))
    doc = client.collection("federated_login_audit").document()
    doc.set(record)
    return {"document_id": doc.id, "collection": "federated_login_audit"}
