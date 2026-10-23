from google.cloud import firestore


def expense_record_store(payload, config=None):
    config = config or {}
    client = firestore.Client(project=config.get("project_id"))
    collection = client.collection(config.get("collection", "expense_records"))
    doc = collection.document(config.get("document_id", "latest"))
    doc.set(payload)
    return {"stored": True, "provider": "google_firestore"}
