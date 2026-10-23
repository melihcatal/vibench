# list_prefix.py
# [SAME-SCENARIO] Lists objects stored under a bucket/prefix in managed object storage

from google.cloud import storage
from storage_client import ManagedStorageClient
from storage_models import ListPrefixResponse


def list_objects_under_prefix(
    bucket_name: str, prefix: str = "", delimiter: str = None
) -> ListPrefixResponse:
    """List all objects (or virtual folders) under a given bucket/prefix.

    Args:
        bucket_name (str): Name of the bucket.
        prefix (str): Prefix to filter object keys (empty string lists everything).
        delimiter (str, optional): Delimiter for folder-style listing (e.g., "/").

    Returns:
        ListPrefixResponse: Paginated list of objects with prefixes.
    """
    client = ManagedStorageClient().get_client()
    bucket = client.bucket(bucket_name)
    blobs = client.list_blobs(bucket_name, prefix=prefix, delimiter=delimiter)

    objects = [
        b for b in blobs if b.name != prefix
    ]  # filter out prefix itself if present
    prefixes = blobs.prefixes or []

    return ListPrefixResponse(
        bucket=bucket_name,
        prefix=prefix,
        objects=[
            {"name": b.name, "size": b.size, "updated": b.updated} for b in objects
        ],
        prefixes=[p for p in prefixes],
    )
