# presigned_download.py
import os
from google.cloud import storage
from storage_models import normalize_object_name
from storage_client import get_client, bucket_name

SERVICE = "Google Cloud Storage"


def presigned_download(object_name: str, expires_seconds: int = 60 * 60 * 24) -> str:
    """Create a time-limited signed download URL for a stored object.\n    Default expiration is 24 hours."""
    client = get_client()
    bucket = client.bucket(bucket_name())
    blob = bucket.blob(normalize_object_name(object_name))
    url = blob.generate_signed_url(
        version="v4",
        expiration=expires_seconds,
        method="GET",
    )
    return url
