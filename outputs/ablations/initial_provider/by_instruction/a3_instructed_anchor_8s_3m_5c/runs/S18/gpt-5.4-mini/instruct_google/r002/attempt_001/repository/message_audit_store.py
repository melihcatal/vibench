from google.cloud import firestore


def message_audit_store(record_id, record):
    client = firestore.Client()
    client.collection("message_audit").document(str(record_id)).set(record)
    return {"provider": "google-firestore", "stored": True, "record_id": str(record_id)}
