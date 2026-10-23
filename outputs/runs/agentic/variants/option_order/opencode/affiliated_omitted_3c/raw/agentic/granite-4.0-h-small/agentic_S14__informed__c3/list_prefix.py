# list_prefix.py
import os
from google.cloud import storage
from storage_models import normalize_object_name
from storage_client import get_client, bucket_name

SERVICE = "Google Cloud Storage"


def list_prefix(prefix: str = "") -> list[dict]:
    """List all objects under a bucket or container prefix."""
    client = get_client()
    bucket = client.bucket(bucket_name())
    blobs = bucket.list_blobs(prefix=prefix)
    return [blob.to_dict() for blob in blobs]
