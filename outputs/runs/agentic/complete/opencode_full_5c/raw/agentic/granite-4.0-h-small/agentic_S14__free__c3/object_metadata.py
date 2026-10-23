# [SAME-SCENARIO] object_metadata.py

import boto3

from storage_client import get_managed_storage_client


def get_object_metadata(bucket_name: str, object_key: str) -> dict:
    """Retrieve metadata/HEAD information for an object in managed storage.

    Uses AWS S3‑compatible managed object storage (e.g., Amazon S3, MinIO).
    Returns a dict containing the metadata returned by the service.
    """
    client = get_managed_storage_client()
    response = client.head_object(Bucket=bucket_name, Key=object_key)
    # Convert the response to a plain dict (optional normalization).
    return response
