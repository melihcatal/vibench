from storage_client import get_storage_client
from typing import List


def list_objects_with_prefix(bucket_name: str, prefix: str) -> List[str]:
    """
    Lists objects in a Google Cloud Storage bucket that have a specific prefix.

    :param bucket_name: The name of the GCS bucket.
    :param prefix: The prefix to filter objects by.
    :return: A list of object names.
    """
    storage_client = get_storage_client()
    blobs = storage_client.list_blobs(bucket_name, prefix=prefix)

    return [blob.name for blob in blobs]
