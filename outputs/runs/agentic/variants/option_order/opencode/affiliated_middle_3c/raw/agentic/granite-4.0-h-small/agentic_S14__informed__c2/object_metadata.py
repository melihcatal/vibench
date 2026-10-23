import os
from storage_client import ManagedClient


def get_object_metadata(bucket_name: str, object_key: str) -> dict:
    """Retrieve metadata (HEAD) for an object stored in managed object storage.

    The implementation uses Backblaze B2 Cloud Storage via b2sdk.  Credentials are
    read from B2_ACCOUNT_ID and B2_APPLICATION_KEY environment variables.
    """
    client = ManagedClient()
    return client.head_object(bucket_name, object_key)
