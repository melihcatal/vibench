import os

from google.cloud import firestore


def login_audit_store(record: dict, collection_name: str = "federated_login_audit") -> str:
    client = firestore.Client(project=os.environ.get("GOOGLE_CLOUD_PROJECT"))
    doc = client.collection(collection_name).document()
    doc.set(record)
    return doc.id
