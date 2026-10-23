import os
from typing import Any, Dict, Optional

from google.cloud import firestore


def get_project_id() -> Optional[str]:
    return os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCLOUD_PROJECT")


def get_firestore_client() -> firestore.Client:
    project_id = get_project_id()
    return firestore.Client(project=project_id) if project_id else firestore.Client()


def collection_ref(client: Optional[firestore.Client], collection: str):
    db = client or get_firestore_client()
    return db.collection(collection)


def serialize_snapshot(snapshot: Any) -> Dict[str, Any]:
    if not snapshot.exists:
        return {}
    data = snapshot.to_dict() or {}
    data["id"] = snapshot.id
    return data
