from typing import Any, Dict

from google.cloud import firestore


def login_audit_store(record: Dict[str, Any], project_id: str, collection_name: str = "federated_login_audit") -> Dict[str, Any]:
    db = firestore.Client(project=project_id)
    doc = db.collection(collection_name).document()
    doc.set(record)
    return {"document_id": doc.id, "collection": collection_name, "provider": "google-cloud-firestore"}
