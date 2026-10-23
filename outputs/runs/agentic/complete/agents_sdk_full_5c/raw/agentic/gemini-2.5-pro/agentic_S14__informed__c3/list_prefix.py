from google.cloud import storage
from .storage_client import get_storage_client, get_bucket_name

def list_objects_with_prefix(prefix: str, delimiter: str | None = None) -> list[str]:
    """
    Lists objects in a Google Cloud Storage bucket that start with a given prefix.

    Args:
        prefix (str): The prefix to filter objects by.
        delimiter (str | None): Delimiter to use for directory-like listing.

    Returns:
        list[str]: A list of object names matching the prefix.
    """
    storage_client = get_storage_client()
    bucket_name = get_bucket_name()

    blobs = storage_client.list_blobs(bucket_name, prefix=prefix, delimiter=delimiter)

    return [blob.name for blob in blobs]
