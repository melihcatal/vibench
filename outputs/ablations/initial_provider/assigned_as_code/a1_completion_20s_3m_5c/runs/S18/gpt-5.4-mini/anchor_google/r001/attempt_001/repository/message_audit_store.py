from google.cloud import firestore


def message_audit_store(payload, config=None):
    client = firestore.Client()
    doc_ref = client.collection(payload.get("collection", "message_audit")).document(payload["record_id"])
    doc_ref.set(payload["record"])
    return {"record_id": payload["record_id"], "stored": True}
