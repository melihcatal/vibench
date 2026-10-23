from google.cloud import storage
from . import storage_client
import os

def upload_file_bytes(object_name: str, data: bytes, content_type: str = "application/octet-stream"):
    """Uploads a byte stream to a GCS bucket."""
    
    gcs_client = storage_client.get_storage_client()
    bucket_name = storage_client.get_default_bucket_name()
    if not bucket_name:
        raise ValueError("GCS_BUCKET_NAME environment variable not set.")

    bucket = gcs_client.bucket(bucket_name)
    blob = bucket.blob(object_name)

    blob.upload_from_string(
        data=data,
        content_type=content_type
    )

    print(f"Bytes uploaded to gs://{bucket_name}/{object_name}")
    return f"gs://{bucket_name}/{object_name}"
