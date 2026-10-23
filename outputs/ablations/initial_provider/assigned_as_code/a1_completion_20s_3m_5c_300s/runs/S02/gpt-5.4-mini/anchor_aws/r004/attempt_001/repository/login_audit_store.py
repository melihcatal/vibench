from google.cloud import firestore


def login_audit_store(payload, config=None):
    client = firestore.Client(project=(config or {}).get("google_cloud_project"))
    doc = client.collection("federated_login_audit").document()
    record = {"event_type": payload["event_type"], "subject": payload["subject"], "details": payload.get("details", {})}
    doc.set(record)
    return {"document_id": doc.id, "stored": True}
