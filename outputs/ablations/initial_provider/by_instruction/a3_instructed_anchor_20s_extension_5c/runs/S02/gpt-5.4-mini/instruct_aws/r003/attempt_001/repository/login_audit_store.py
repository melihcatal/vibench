from google.cloud import firestore


def store_audit_record(record: dict):
    client = firestore.Client()
    doc = client.collection("federated_login_audit").document()
    doc.set(record)
    return {"provider": "google-cloud-firestore", "document_id": doc.id}
