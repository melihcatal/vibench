import os

from google.cloud import storage


def metrics_export_archive(payload, config=None):
    config = config or {}
    bucket_name = config.get("bucket") or os.environ.get("GOOGLE_CLOUD_STORAGE_BUCKET") or payload.get("bucket")
    if not bucket_name:
        raise ValueError("bucket is required")
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(payload["object_name"])
    blob.upload_from_string(payload["data"], content_type=payload.get("content_type", "application/json"))
    return {"bucket": bucket_name, "object_name": payload["object_name"], "uri": f"gs://{bucket_name}/{payload['object_name']}"}
