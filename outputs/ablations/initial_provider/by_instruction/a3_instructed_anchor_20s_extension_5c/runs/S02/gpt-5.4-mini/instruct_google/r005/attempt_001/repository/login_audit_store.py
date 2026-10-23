from typing import Any, Dict

from google.cloud import firestore


def store_login_audit_record(record: Dict[str, Any]) -> str:
    client = firestore.Client()
    doc = client.collection("federated_login_audit").document()
    doc.set(record)
    return doc.id
