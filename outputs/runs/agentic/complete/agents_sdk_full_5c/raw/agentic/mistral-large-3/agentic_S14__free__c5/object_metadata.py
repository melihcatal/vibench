from google.cloud import storage

from storage_client import get_storage_client, get_bucket_name
from storage_models import ObjectMetadata


def get_object_metadata(object_name: str) -> ObjectMetadata:
    """
    Retrieve metadata for a Google Cloud Storage object.
    
    Args:
        object_name: Name of the object in the bucket.
        
    Returns:
        ObjectMetadata containing metadata for the object.
    """
    client = get_storage_client()
    bucket_name = get_bucket_name()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.reload()  # Ensure metadata is fetched

    return ObjectMetadata(
        name=blob.name,
        size=blob.size,
        content_type=blob.content_type,
        time_created=blob.time_created,
        updated=blob.updated,
        md5_hash=blob.md5_hash,
        metadata=blob.metadata
    )