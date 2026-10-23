import os

from google.cloud import firestore


def expense_record_store(payload, config=None):
    config = config or {}
    client = firestore.Client(project=config.get("project_id") or os.environ.get("GOOGLE_CLOUD_PROJECT"))
    collection = config.get("collection", "expenses")
    doc = client.collection(collection).document()
    doc.set(payload)
    return {"document_id": doc.id, "stored": True}
