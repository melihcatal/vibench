import os
from typing import Any, Dict

from google.cloud import firestore

from identity_client import get_firestore_client


def persist_login_audit(record: Dict[str, Any]) -> str:
    client = get_firestore_client()
    collection = os.environ.get("FIRESTORE_AUDIT_COLLECTION", "federated_login_audit")
    doc = client.collection(collection).document()
    doc.set(record)
    return doc.id
