import os
from google.cloud import firestore
from google.cloud import storage


def load_config(config=None):
    config = config or {}
    merged = dict(config)
    merged.setdefault("project_id", os.environ.get("GOOGLE_CLOUD_PROJECT"))
    merged.setdefault("collection", os.environ.get("FIRESTORE_COLLECTION", "documents"))
    merged.setdefault("bucket", os.environ.get("GCS_BUCKET"))
    return merged


def get_firestore_client(config=None):
    config = load_config(config)
    return firestore.Client(project=config["project_id"])


def get_storage_client(config=None):
    config = load_config(config)
    return storage.Client(project=config["project_id"])
