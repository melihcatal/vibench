import os
from functools import lru_cache
from typing import Any, Dict

from google.cloud import firestore


def _env(name: str, default: str = "") -> str:
    value = os.getenv(name, default)
    return value.strip()


@lru_cache(maxsize=1)
def get_settings() -> Dict[str, str]:
    return {
        "project_id": _env("GOOGLE_CLOUD_PROJECT", _env("GCLOUD_PROJECT", "")),
        "collection": _env("FIRESTORE_COLLECTION", "documents"),
        "archive_bucket": _env("GCS_ARCHIVE_BUCKET", "document-archives"),
    }


@lru_cache(maxsize=1)
def get_firestore_client() -> firestore.Client:
    settings = get_settings()
    if settings["project_id"]:
        return firestore.Client(project=settings["project_id"])
    return firestore.Client()


def get_collection_name() -> str:
    return get_settings()["collection"]


def document_ref(document_id: str):
    return (
        get_firestore_client().collection(get_collection_name()).document(document_id)
    )


def collection_ref():
    return get_firestore_client().collection(get_collection_name())


def normalize_for_firestore(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): normalize_for_firestore(v) for k, v in value.items()}
    if isinstance(value, list):
        return [normalize_for_firestore(v) for v in value]
    return value
