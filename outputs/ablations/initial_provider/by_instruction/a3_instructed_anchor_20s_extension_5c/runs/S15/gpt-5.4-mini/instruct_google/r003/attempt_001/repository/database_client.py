import os
from functools import lru_cache

from google.cloud import firestore


@lru_cache(maxsize=1)
def get_client() -> firestore.Client:
    project = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCLOUD_PROJECT")
    return firestore.Client(project=project)


def get_collection(name: str):
    return get_client().collection(name)
