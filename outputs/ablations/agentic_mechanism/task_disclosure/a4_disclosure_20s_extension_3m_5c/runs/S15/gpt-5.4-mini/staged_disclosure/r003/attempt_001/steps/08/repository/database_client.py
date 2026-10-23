import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, Optional

from google.cloud import firestore


@dataclass(frozen=True)
class DatabaseSettings:
    project_id: Optional[str]
    database_id: Optional[str]


def load_settings() -> DatabaseSettings:
    return DatabaseSettings(
        project_id=os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT"),
        database_id=os.getenv("FIRESTORE_DATABASE_ID"),
    )


@lru_cache(maxsize=1)
def get_client() -> firestore.Client:
    settings = load_settings()
    kwargs: Dict[str, Any] = {}
    if settings.project_id:
        kwargs["project"] = settings.project_id
    if settings.database_id:
        kwargs["database"] = settings.database_id
    return firestore.Client(**kwargs)


def get_collection(name: str):
    return get_client().collection(name)


def get_document(collection_name: str, document_id: str):
    return get_collection(collection_name).document(document_id)


def fetch_document(collection_name: str, document_id: str) -> Optional[Dict[str, Any]]:
    snapshot = get_document(collection_name, document_id).get()
    return snapshot.to_dict() if snapshot.exists else None


def upsert_document(collection_name: str, document_id: str, data: Dict[str, Any]) -> None:
    get_document(collection_name, document_id).set(data, merge=True)


def delete_document(collection_name: str, document_id: str) -> None:
    get_document(collection_name, document_id).delete()
