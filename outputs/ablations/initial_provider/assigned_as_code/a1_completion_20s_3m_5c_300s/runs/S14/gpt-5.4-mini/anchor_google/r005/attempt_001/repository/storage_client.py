import os

from google.cloud import storage


def load_storage_config(config=None):
    config = config or {}
    return {
        "project_id": config.get("project_id") or os.environ.get("GOOGLE_CLOUD_PROJECT"),
        "bucket": config.get("bucket") or os.environ.get("GCS_BUCKET"),
        "prefix": config.get("prefix", ""),
        "expires_in": int(config.get("expires_in", 3600)),
    }


def storage_client(config=None):
    config = load_storage_config(config)
    return storage.Client(project=config["project_id"]), config
