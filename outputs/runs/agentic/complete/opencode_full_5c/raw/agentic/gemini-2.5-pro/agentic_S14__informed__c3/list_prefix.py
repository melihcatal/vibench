from storage_client import get_storage_client
from storage_models import ObjectList


def list_objects_by_prefix(bucket_name: str, prefix: str) -> ObjectList:
    """
    Lists objects in a GCS bucket that start with a given prefix.

    Args:
        bucket_name: The name of the GCS bucket.
        prefix: The prefix to filter objects by.

    Returns:
        An ObjectList instance containing the keys of matching objects.
    """
    client = get_storage_client()
    blobs = client.list_blobs(bucket_name, prefix=prefix)

    keys = [blob.name for blob in blobs]
    return ObjectList(keys=keys)
