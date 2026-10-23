import os
from functools import lru_cache

from google.cloud import firestore


def _env(name, default=None):
    value = os.getenv(name)
    return value if value not in (None, "") else default


def project_id():
    return _env("GOOGLE_CLOUD_PROJECT") or _env("GCLOUD_PROJECT") or _env("FIRESTORE_PROJECT")


def collection_name():
    return _env("FIRESTORE_COLLECTION", "documents")


@lru_cache(maxsize=1)
def get_client():
    kwargs = {}
    pid = project_id()
    if pid:
        kwargs["project"] = pid
    return firestore.Client(**kwargs)


def get_collection():
    return get_client().collection(collection_name())


def document_ref(document_id):
    return get_collection().document(str(document_id))
