from google.cloud import firestore


def message_audit_store(payload, config=None):
    client = firestore.Client()
    collection = client.collection((config or {}).get("collection", "message_audit"))
    record = dict(payload or {})
    doc = collection.document(record.get("message_id", "unknown"))
    doc.set(record)
    return {"stored": True, "message_id": record.get("message_id", "unknown")}
