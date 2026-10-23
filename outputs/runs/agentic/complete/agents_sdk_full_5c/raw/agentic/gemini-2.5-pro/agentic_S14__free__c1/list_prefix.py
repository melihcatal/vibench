from typing import List
from storage_client import get_gcs_client, get_bucket_name

def list_blobs_with_prefix(prefix: str, delimiter: str = None) -> List[str]:
    """
    Lists blobs in a GCS bucket that begin with a specific prefix.

    Args:
        prefix (str): The prefix to filter by.
        delimiter (str, optional): If provided, results are grouped by common prefixes.
                                  For example, using '/' can simulate directories.

    Returns:
        A list of blob names matching the prefix.
    """
    client = get_gcs_client()
    bucket_name = get_bucket_name()

    blobs = client.list_blobs(bucket_name, prefix=prefix, delimiter=delimiter)

    return [blob.name for blob in blobs]
