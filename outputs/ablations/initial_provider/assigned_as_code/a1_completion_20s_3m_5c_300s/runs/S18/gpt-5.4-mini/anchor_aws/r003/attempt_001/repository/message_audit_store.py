from google.cloud import firestore


def message_audit_store(payload, config=None):
    client = firestore.Client()
    collection = (config or {}).get("collection", "message_audit")
    doc_id = payload.get("id") or payload.get("message_id")
    client.collection(collection).document(str(doc_id)).set(payload)
    return {"stored": True, "id": str(doc_id)}
