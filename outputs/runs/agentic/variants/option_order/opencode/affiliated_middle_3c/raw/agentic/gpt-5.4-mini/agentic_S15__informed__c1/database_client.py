import os
from dataclasses import dataclass

from google.cloud import firestore


@dataclass(frozen=True)
class DatabaseConfig:
    project_id: str | None
    collection_name: str


def load_config() -> DatabaseConfig:
    return DatabaseConfig(
        project_id=os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT"),
        collection_name=os.getenv("FIRESTORE_COLLECTION", "documents"),
    )


def get_client() -> firestore.Client:
    return firestore.Client(project=load_config().project_id)


def get_collection(client: firestore.Client | None = None):
    cfg = load_config()
    db = client or get_client()
    return db.collection(cfg.collection_name)
