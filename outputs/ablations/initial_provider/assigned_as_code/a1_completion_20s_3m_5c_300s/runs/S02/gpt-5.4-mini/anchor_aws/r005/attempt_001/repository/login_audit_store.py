from google.cloud import firestore


def login_audit_store(payload, config=None):
    client = firestore.Client(project=(config or {}).get("gcp_project"))
    collection = (config or {}).get("collection", "federated_login_audit")
    doc = client.collection(collection).document()
    record = dict(payload)
    doc.set(record)
    return {"document_id": doc.id, "stored": True}
