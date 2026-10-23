import os

from google.cloud import firestore
from google.cloud import storage


def load_config(config=None):
    config = config or {}
    return {
        "project_id": config.get("project_id") or os.environ["GOOGLE_CLOUD_PROJECT"],
        "collection": config.get("collection") or os.environ["FIRESTORE_COLLECTION"],
        "bucket": config.get("bucket") or os.environ.get("GCS_BUCKET"),
    }


def firestore_client(config=None):
    return firestore.Client(project=load_config(config)["project_id"])


def storage_client(config=None):
    return storage.Client(project=load_config(config)["project_id"])
