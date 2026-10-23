from typing import List
from storage_client import get_gcs_client, get_storage_bucket


def list_objects_by_prefix(bucket_name: str, prefix: str) -> List[str]:
    """
    Lists objects in a GCS bucket that start with a given prefix.

    Args:
        bucket_name: The name of the GCS bucket.
        prefix: The prefix to filter objects by.

    Returns:
        A list of object names matching the prefix.
    """
    client = get_gcs_client()
    blobs = client.list_blobs(bucket_name, prefix=prefix)
    return [blob.name for blob in blobs]
