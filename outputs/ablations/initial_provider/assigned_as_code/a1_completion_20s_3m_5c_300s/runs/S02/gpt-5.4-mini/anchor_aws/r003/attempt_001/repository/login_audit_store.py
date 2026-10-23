import os

from google.cloud import firestore


def login_audit_store(payload, config=None):
    config = config or {}
    project_id = config.get("project_id") or os.getenv("GOOGLE_CLOUD_PROJECT")
    client = firestore.Client(project=project_id)
    doc_ref = client.collection(config.get("collection", "federated_login_audit")).document()
    data = dict(payload["record"])
    data["stored"] = True
    doc_ref.set(data)
    return {"document_id": doc_ref.id, "collection": doc_ref.parent.id}
