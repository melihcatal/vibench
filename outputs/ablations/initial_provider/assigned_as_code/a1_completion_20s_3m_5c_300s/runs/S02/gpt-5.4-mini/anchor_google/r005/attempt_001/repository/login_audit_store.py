from google.cloud import firestore


def login_audit_store(payload, config=None):
    config = dict(config or {})
    client = firestore.Client(project=config.get("project_id"))
    collection = config.get("collection", "federated_login_audit")
    doc = client.collection(collection).document(payload.get("event_id") or "latest")
    doc.set(payload)
    return {"stored": True, "document_id": doc.id, "collection": collection}
