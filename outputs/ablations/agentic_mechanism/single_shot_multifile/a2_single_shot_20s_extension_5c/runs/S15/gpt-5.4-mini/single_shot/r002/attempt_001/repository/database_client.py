from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

from google.cloud import firestore

DEFAULT_COLLECTION_NAME = os.getenv("FIRESTORE_COLLECTION", "documents")


def get_collection_name() -> str:
    return os.getenv("FIRESTORE_COLLECTION", DEFAULT_COLLECTION_NAME)


@lru_cache(maxsize=1)
def get_firestore_client() -> firestore.Client:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCLOUD_PROJECT")
    if project_id:
        return firestore.Client(project=project_id)
    return firestore.Client()
