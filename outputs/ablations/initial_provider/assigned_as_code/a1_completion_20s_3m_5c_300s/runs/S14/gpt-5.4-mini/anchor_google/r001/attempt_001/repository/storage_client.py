import os

from google.cloud import storage


def load_storage_config(config=None):
    config = config or {}
    return {
        "project_id": config.get("project_id", os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT")),
        "bucket": config.get("bucket", os.environ.get("STORAGE_BUCKET")),
    }


def get_storage_client(config=None):
    cfg = load_storage_config(config)
    return storage.Client(project=cfg["project_id"]), cfg


def get_bucket(config=None):
    client, cfg = get_storage_client(config)
    return client.bucket(cfg["bucket"]), cfg


def get_blob(object_name, config=None):
    bucket, cfg = get_bucket(config)
    return bucket.blob(object_name), cfg
