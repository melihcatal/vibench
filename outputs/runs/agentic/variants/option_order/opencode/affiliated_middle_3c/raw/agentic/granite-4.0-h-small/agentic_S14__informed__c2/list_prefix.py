import os
from storage_client import ManagedClient


def list_objects_under_prefix(
    bucket_name: str, prefix: str = "", max_results: int = 1000
):
    """List objects stored under a bucket/container prefix.

    Uses Backblaze B2 Cloud Storage (b2sdk).  The function calls the B2 'list' API
    repeatedly if the prefix contains many objects.  Credentials are sourced from
    B2_ACCOUNT_ID and B2_APPLICATION_KEY.
    """
    client = ManagedClient()
    return client.list_objects(bucket_name, prefix=prefix, max_results=max_results)
