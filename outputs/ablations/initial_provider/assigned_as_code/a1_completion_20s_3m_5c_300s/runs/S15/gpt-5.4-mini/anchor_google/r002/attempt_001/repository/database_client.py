import os
from google.cloud import firestore
from google.cloud import storage


def load_config(config=None):
    config = config or {}
    merged = {
        "project_id": config.get("project_id") or os.environ["GOOGLE_CLOUD_PROJECT"],
        "collection": config.get("collection") or os.environ.get("FIRESTORE_COLLECTION", "documents"),
        "bucket": config.get("bucket") or os.environ.get("GCS_BUCKET"),
    }
    return merged


def get_firestore_client(config=None):
    config = load_config(config)
    return firestore.Client(project=config["project_id"])


def get_storage_client(config=None):
    config = load_config(config)
    return storage.Client(project=config["project_id"])
