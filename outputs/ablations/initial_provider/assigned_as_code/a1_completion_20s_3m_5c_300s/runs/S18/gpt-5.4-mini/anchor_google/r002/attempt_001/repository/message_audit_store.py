from google.cloud import firestore


def message_audit_store(payload, config=None):
    client = firestore.Client()
    doc = client.collection("message_audit").document(payload["message_id"])
    doc.set(payload)
    return {"stored": True, "message_id": payload["message_id"]}
