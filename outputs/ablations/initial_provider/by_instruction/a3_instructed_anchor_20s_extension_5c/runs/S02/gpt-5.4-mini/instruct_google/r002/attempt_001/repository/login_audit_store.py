from typing import Mapping

from google.cloud import firestore


def login_audit_store(record: Mapping[str, object]) -> dict[str, object]:
    client = firestore.Client()
    doc = client.collection("federated_login_audit").document()
    doc.set(dict(record))
    return {"provider": "google-cloud-firestore", "document_id": doc.id}
