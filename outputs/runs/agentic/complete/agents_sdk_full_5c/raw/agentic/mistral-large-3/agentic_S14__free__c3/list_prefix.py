from typing import List
from google.cloud import storage
from storage_client import get_storage_client, get_bucket_name


def list_objects_with_prefix(prefix: str) -> List[str]:
    """
    List stored objects under a Google Cloud Storage bucket prefix.
    Returns a list of object names.
    """
    client = get_storage_client()
    bucket_name = get_bucket_name()
    bucket = client.bucket(bucket_name)

    blobs = bucket.list_blobs(prefix=prefix)
    return [blob.name for blob in blobs]