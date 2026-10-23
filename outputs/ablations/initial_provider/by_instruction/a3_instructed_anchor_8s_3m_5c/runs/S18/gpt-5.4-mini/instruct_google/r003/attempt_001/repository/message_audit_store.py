from google.cloud import firestore


def message_audit_store(record):
    client = firestore.Client()
    doc = client.collection("message_audit").document(record.get("message_id") or record.get("id") or "unknown")
    doc.set(record)
    return {"provider": "google.firestore", "document_id": doc.id}
