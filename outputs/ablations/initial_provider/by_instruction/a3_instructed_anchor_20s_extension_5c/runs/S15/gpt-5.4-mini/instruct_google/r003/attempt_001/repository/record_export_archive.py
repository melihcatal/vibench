import os

from google.cloud import storage


def record_export_archive(bucket_name: str, object_name: str, content: bytes) -> dict:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.upload_from_string(content)
    return {"bucket": bucket_name, "object_name": object_name, "provider": "google_cloud_storage"}
