from google.cloud import firestore


def login_audit_store(payload, config=None):
    client = firestore.Client(project=config.get("project_id"))
    doc = client.collection("federated_login_audit").document()
    doc.set(payload["record"])
    return {"document_id": doc.id}
