import os
from google.cloud import firestore


def expense_record_store(payload, config=None):
    config = config or {}
    client = firestore.Client(project=config.get("project_id") or os.environ.get("GOOGLE_CLOUD_PROJECT"))
    collection = config.get("collection", "expense_records")
    data = payload.get("record", payload)
    doc_ref = client.collection(collection).document(config.get("document_id") or data.get("id") or client.collection(collection).document().id)
    doc_ref.set(data)
    return {"document_id": doc_ref.id, "collection": collection}
