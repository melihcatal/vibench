import os

from google.cloud import storage


def load_config(config=None):
    config = config or {}
    project_id = config.get("project_id") or os.getenv("GCS_PROJECT_ID") or os.getenv("GOOGLE_CLOUD_PROJECT")
    bucket = config.get("bucket") or os.getenv("GCS_BUCKET")
    if not project_id:
        raise ValueError("project_id is required")
    if not bucket:
        raise ValueError("bucket is required")
    merged = dict(config)
    merged["project_id"] = project_id
    merged["bucket"] = bucket
    return merged


def get_client(config=None):
    config = load_config(config)
    return storage.Client(project=config["project_id"])


def get_bucket(config=None):
    config = load_config(config)
    client = get_client(config)
    return client.bucket(config["bucket"])
