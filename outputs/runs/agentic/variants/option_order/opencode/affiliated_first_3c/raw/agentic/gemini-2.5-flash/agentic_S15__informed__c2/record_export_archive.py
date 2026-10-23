import os
from google.cloud import storage


def record_export_archive(bucket_name: str, blob_name: str, data: bytes):
    client = storage.Client(project=os.getenv("GOOGLE_CLOUD_PROJECT"))
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.upload_from_string(data, content_type="application/json")

    return {
        "status": "success",
        "bucket": bucket_name,
        "blob": blob_name,
        "uri": blob.public_url,
    }
