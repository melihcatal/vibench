from storage_client import get_storage_client, get_gcs_bucket_name
from storage_models import ObjectMetadata


def get_object_metadata(object_name: str) -> ObjectMetadata:
    """
    Retrieves metadata for an object in Google Cloud Storage.

    Args:
        object_name: The name of the object.

    Returns:
        An ObjectMetadata object.
    """
    storage_client = get_storage_client()
    bucket_name = get_gcs_bucket_name()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.get_blob(object_name)

    if not blob:
        raise FileNotFoundError(
            f"Object '{object_name}' not found in bucket '{bucket_name}'."
        )

    blob.reload()

    return ObjectMetadata(
        name=blob.name,
        bucket=blob.bucket.name,
        size=blob.size,
        content_type=blob.content_type,
        create_time=blob.time_created.isoformat(),
        update_time=blob.updated.isoformat(),
        custom_metadata=blob.metadata,
    )
