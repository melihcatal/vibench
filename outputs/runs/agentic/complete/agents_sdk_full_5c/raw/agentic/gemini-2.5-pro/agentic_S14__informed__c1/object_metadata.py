from google.cloud.storage import Blob
from storage_client import get_storage_client, get_default_bucket_name
from storage_models import StorageObject

def get_object_metadata(blob_name: str) -> StorageObject:
    """
    Retrieves metadata for a specific object in a GCS bucket.

    Args:
        blob_name (str): The name of the blob in the bucket.

    Returns:
        StorageObject: A data class containing the object's metadata.
    """
    client = get_storage_client()
    bucket_name = get_default_bucket_name()
    bucket = client.bucket(bucket_name)
    blob: Blob = bucket.get_blob(blob_name)

    if not blob:
        raise FileNotFoundError(f"Blob {blob_name} not found in bucket {bucket_name}.")

    return StorageObject(
        name=blob.name,
        bucket=blob.bucket.name,
        size=blob.size,
        content_type=blob.content_type,
        updated=blob.updated,
    )
