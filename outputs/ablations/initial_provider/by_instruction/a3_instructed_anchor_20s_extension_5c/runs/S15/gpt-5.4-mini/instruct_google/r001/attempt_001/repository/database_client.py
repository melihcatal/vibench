import os
from typing import Any, Dict, Optional

from google.cloud import firestore


def get_project_id() -> Optional[str]:
    return os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCLOUD_PROJECT")


def get_firestore_client() -> firestore.Client:
    project_id = get_project_id()
    return firestore.Client(project=project_id) if project_id else firestore.Client()


def get_collection_name(default: str = "documents") -> str:
    return os.getenv("FIRESTORE_COLLECTION", default)


def document_ref(client: firestore.Client, collection: str, document_id: str):
    return client.collection(collection).document(document_id)


def collection_ref(client: firestore.Client, collection: str):
    return client.collection(collection)


def serialize_result(document: Optional[Dict[str, Any]] = None, documents=None, error: Optional[str] = None) -> Dict[str, Any]:
    return {"ok": error is None, "document": document, "documents": documents, "error": error}
