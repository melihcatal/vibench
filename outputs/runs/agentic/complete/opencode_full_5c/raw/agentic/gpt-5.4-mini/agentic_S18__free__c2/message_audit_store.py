from google.cloud import firestore


def store_message_audit(record_id: str, payload: dict) -> str:
    client = firestore.Client()
    client.collection("message_audit").document(record_id).set(payload)
    return record_id


def fetch_message_audit(record_id: str) -> dict:
    client = firestore.Client()
    snapshot = client.collection("message_audit").document(record_id).get()
    return snapshot.to_dict() or {}
