from google.cloud import firestore


def message_audit_store(payload, config=None):
    config = config or {}
    client = firestore.Client(project=config.get("project_id"))
    collection = client.collection(config.get("collection", "message_audit"))
    document = collection.document(payload.get("message_id") or payload.get("id") or "unknown")
    document.set(payload)
    return {"provider": "google_cloud_firestore", "stored": True, "message_id": document.id}
