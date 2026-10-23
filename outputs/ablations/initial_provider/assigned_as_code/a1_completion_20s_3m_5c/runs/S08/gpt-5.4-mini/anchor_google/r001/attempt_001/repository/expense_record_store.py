from google.cloud import firestore

from document_models import normalize_expense_record


def expense_record_store(payload, config=None):
    config = config or {}
    client = firestore.Client(project=config["project_id"])
    record = normalize_expense_record(payload)
    doc_ref = client.collection(config.get("collection", "expense_records")).document(config.get("document_id") or "auto")
    doc_ref.set(record)
    return {"stored": True, "document_id": doc_ref.id, "provider": "google.cloud.firestore"}
