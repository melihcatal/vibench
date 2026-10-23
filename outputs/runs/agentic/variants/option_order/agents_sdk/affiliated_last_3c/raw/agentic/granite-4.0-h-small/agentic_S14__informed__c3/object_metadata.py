import os
from google.cloud import storage
from storage_client import get_storage_client

def object_metadata(bucket_name, blob_name):
    """Retrieve metadata for an object in Google Cloud Storage.

    Args:
        bucket_name (str): Bucket name.
        blob_name (str): Object (blob) name.

    Returns:
        dict: Parsed JSON metadata of the object.
    """
    client = get_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    metadata = blob.metadata or {}
    # Force a HEAD request to populate common metadata fields
    blob.reload()
    return {
        "name": blob.name,
        "size": blob.size,
        "content_type": blob.content_type,
        "created": blob.time_created.isoformat() if blob.time_created else None,
        "updated": blob.time_updated.isoformat() if blob.time_updated else None,
        "metadata": metadata,
    }
