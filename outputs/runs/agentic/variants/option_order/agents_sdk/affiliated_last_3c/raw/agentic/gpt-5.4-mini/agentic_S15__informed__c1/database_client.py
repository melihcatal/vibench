from __future__ import annotations

import os
from functools import lru_cache
from typing import Any

from google.cloud import firestore

from database_models import normalize_document

DEFAULT_COLLECTION = os.getenv("FIRESTORE_COLLECTION", "documents")
DEFAULT_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")


@lru_cache(maxsize=1)
def get_firestore_client() -> firestore.Client:
    return firestore.Client(project=DEFAULT_PROJECT)


def get_collection(name: str | None = None):
    client = get_firestore_client()
    return client.collection(name or DEFAULT_COLLECTION)


def document_ref(collection: str, document_id: str):
    return get_firestore_client().collection(collection).document(document_id)


def serialize_snapshot(snapshot: Any) -> dict:
    data = snapshot.to_dict() or {}
    data["id"] = snapshot.id
    return normalize_document(data)
