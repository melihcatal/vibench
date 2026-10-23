import os
import time
import uuid
from typing import Any, Dict, Optional

from google.cloud import firestore


def _client() -> firestore.Client:
    project = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCLOUD_PROJECT")
    return firestore.Client(project=project)


def store_login_audit_record(record: Dict[str, Any], collection_name: str = "federated_login_audit") -> Dict[str, Any]:
    client = _client()
    payload = dict(record)
    payload.setdefault("provider", "google")
    payload.setdefault("event_id", str(uuid.uuid4()))
    payload.setdefault("created_at_unix_ms", int(time.time() * 1000))
    payload["document_store_provider"] = "google_cloud_firestore"

    doc_id = payload["event_id"]
    client.collection(collection_name).document(doc_id).set(payload)
    return {"collection": collection_name, "document_id": doc_id, "stored": True, "provider": "google_cloud_firestore"}


def get_login_audit_record(event_id: str, collection_name: str = "federated_login_audit") -> Optional[Dict[str, Any]]:
    client = _client()
    snapshot = client.collection(collection_name).document(event_id).get()
    if not snapshot.exists:
        return None
    data = snapshot.to_dict() or {}
    data["event_id"] = event_id
    return data
