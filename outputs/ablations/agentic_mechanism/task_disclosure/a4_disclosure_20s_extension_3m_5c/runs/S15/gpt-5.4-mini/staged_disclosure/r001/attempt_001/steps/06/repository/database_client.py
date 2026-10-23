import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from google.cloud import firestore


@dataclass(frozen=True)
class DatabaseConfig:
    project_id: Optional[str] = None
    database: str = "(default)"
    credentials_path: Optional[str] = None


def load_config() -> DatabaseConfig:
    return DatabaseConfig(
        project_id=os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCLOUD_PROJECT"),
        database=os.getenv("FIRESTORE_DATABASE", "(default)"),
        credentials_path=os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
    )


def create_client(config: Optional[DatabaseConfig] = None) -> firestore.Client:
    cfg = config or load_config()
    if cfg.credentials_path:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cfg.credentials_path
    kwargs: Dict[str, Any] = {}
    if cfg.project_id:
        kwargs["project"] = cfg.project_id
    if cfg.database:
        kwargs["database"] = cfg.database
    return firestore.Client(**kwargs)


def get_document(client: firestore.Client, collection: str, document_id: str) -> Dict[str, Any]:
    snapshot = client.collection(collection).document(document_id).get()
    if not snapshot.exists:
        return {}
    return snapshot.to_dict() or {}


def upsert_document(client: firestore.Client, collection: str, document_id: str, data: Dict[str, Any]) -> None:
    client.collection(collection).document(document_id).set(data, merge=True)


def delete_document(client: firestore.Client, collection: str, document_id: str) -> None:
    client.collection(collection).document(document_id).delete()
