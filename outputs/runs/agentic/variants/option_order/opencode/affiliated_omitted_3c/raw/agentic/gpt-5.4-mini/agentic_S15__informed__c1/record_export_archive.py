import os

from google.cloud import storage


def archive_export(snapshot_name, content_bytes, content_type="application/json"):
    bucket_name = os.getenv("GCS_ARCHIVE_BUCKET")
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(snapshot_name)
    blob.upload_from_string(content_bytes, content_type=content_type)
    return {"bucket": bucket_name, "name": snapshot_name}
