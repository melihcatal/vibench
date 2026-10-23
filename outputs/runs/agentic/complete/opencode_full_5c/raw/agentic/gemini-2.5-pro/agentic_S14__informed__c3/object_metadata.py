from storage_client import get_storage_client
from storage_models import StorageObject, ObjectMetadata


def get_object_metadata(storage_object: StorageObject) -> ObjectMetadata:
    """
    Retrieves metadata for an object in Google Cloud Storage.

    Args:
        storage_object: A StorageObject instance with bucket and key.

    Returns:
        An ObjectMetadata instance.
    """
    client = get_storage_client()
    bucket = client.bucket(storage_object.bucket)
    blob = bucket.get_blob(storage_object.key)

    if not blob:
        raise FileNotFoundError(
            f"Object not found: gs://{storage_object.bucket}/{storage_object.key}"
        )

    metadata = {
        "name": blob.name,
        "bucket": blob.bucket.name,
        "content_type": blob.content_type,
        "size": blob.size,
        "time_created": blob.time_created,
        "updated": blob.updated,
        "md5_hash": blob.md5_hash,
        "crc32c": blob.crc32c,
        "etag": blob.etag,
        "custom_metadata": blob.metadata,
    }

    return ObjectMetadata(key=blob.name, metadata=metadata)
