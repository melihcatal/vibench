import os
from google.cloud import storage
from storage_client import get_storage_client

def list_prefix(bucket_name, prefix='', delimiter=None, max_results=None):
    """List objects under a bucket with an optional prefix (folder-like behavior).

    Args:
        bucket_name (str): Bucket name.
        prefix (str): Prefix to filter object names (e.g., 'documents/').
        delimiter (str): Character to use for grouping (e.g., '/' to emulate folders).
        max_results (int): Maximum number of results to return.

    Returns:
        list[google.cloud.storage.blob.Blob]: List of matching blobs.
    """
    client = get_storage_client()
    bucket = client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=prefix, delimiter=delimiter, max_results=max_results)
    return list(blobs)
