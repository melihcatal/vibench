import os

from google.cloud import firestore


def expense_record_store(payload, config=None):
    config = config or {}
    client = firestore.Client(project=config.get("project_id") or os.environ.get("GOOGLE_CLOUD_PROJECT"))
    collection_name = config.get("collection") or "expense_records"
    record = payload.get("record") or payload
    doc_ref = client.collection(collection_name).document(record.get("id") or "latest")
    doc_ref.set(record)
    return {"stored": True, "collection": collection_name, "document_id": doc_ref.id}
