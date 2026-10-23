from typing import List
from storage_client import get_storage_client, get_gcs_bucket_name
from storage_models import StorageObject


def list_objects_by_prefix(prefix: str) -> List[StorageObject]:
    """
    Lists objects in a Google Cloud Storage bucket that match a prefix.

    Args:
        prefix: The prefix to filter objects by.

    Returns:
        A list of StorageObject models representing the found objects.
    """
    storage_client = get_storage_client()
    bucket_name = get_gcs_bucket_name()

    blobs = storage_client.list_blobs(bucket_name, prefix=prefix)

    object_list = []
    for blob in blobs:
        object_list.append(
            StorageObject(
                name=blob.name,
                bucket=blob.bucket.name,
                size=blob.size,
                content_type=blob.content_type,
            )
        )
    return object_list
