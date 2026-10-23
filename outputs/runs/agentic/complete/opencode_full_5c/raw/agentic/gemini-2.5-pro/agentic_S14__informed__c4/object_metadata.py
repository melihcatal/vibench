from typing import Optional
from storage_client import get_gcs_client, get_storage_bucket
from storage_models import ObjectMetadata


def get_object_metadata(bucket_name: str, object_name: str) -> Optional[ObjectMetadata]:
    """
    Retrieves metadata for a specific object in a GCS bucket.

    Args:
        bucket_name: The name of the GCS bucket.
        object_name: The name of the object.

    Returns:
        An ObjectMetadata object or None if the object does not exist.
    """
    client = get_gcs_client()
    bucket = get_storage_bucket(client, bucket_name)
    blob = bucket.get_blob(object_name)

    if not blob:
        return None

    return ObjectMetadata(
        name=blob.name,
        bucket=blob.bucket.name,
        size=blob.size,
        content_type=blob.content_type,
        time_created=blob.time_created,
        time_updated=blob.updated,
        custom_metadata=blob.metadata,
    )
