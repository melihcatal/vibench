import os

from google.cloud import storage


def get_storage_client():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "path/to/credentials.json")
    return storage.Client()


def normalize_payload(payload):
    return {
        "bucket": payload.get("bucket", os.getenv("GCS_BUCKET", "default-bucket")),
        "object_name": payload["object_name"],
        "data": payload.get("data"),
        "content_type": payload.get("content_type", "application/octet-stream"),
    }