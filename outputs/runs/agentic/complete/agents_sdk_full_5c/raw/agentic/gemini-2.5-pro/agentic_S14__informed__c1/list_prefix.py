from typing import List
from storage_client import get_storage_client, get_default_bucket_name

def list_objects_with_prefix(prefix: str, delimiter: str = None) -> List[str]:
    """
    Lists objects in a GCS bucket that start with a given prefix.

    Args:
        prefix (str): The prefix to filter by.
        delimiter (str, optional): Delimiter to use for directory-like listing. Defaults to None.

    Returns:
        List[str]: A list of blob names.
    """
    client = get_storage_client()
    bucket_name = get_default_bucket_name()
    
    blobs = client.list_blobs(bucket_name, prefix=prefix, delimiter=delimiter)

    return [blob.name for blob in blobs]
