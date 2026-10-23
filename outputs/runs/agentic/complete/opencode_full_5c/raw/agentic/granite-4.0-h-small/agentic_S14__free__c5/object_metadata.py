# object_metadata.py
# [SAME-SCENARIO] Reads metadata/head information for an object from managed storage

from google.cloud import storage
from storage_client import ManagedStorageClient
from storage_models import ObjectMetadataResponse


def get_object_metadata(bucket_name: str, blob_name: str) -> ObjectMetadataResponse:
    """Retrieve metadata (HEAD request) for a specific object in a bucket.

    Args:
        bucket_name (str): Bucket name.
        blob_name (str): Object name/key.

    Returns:
        ObjectMetadataResponse: Parsed metadata fields.
    """
    client = ManagedStorageClient().get_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # HEAD request - does not download content
    metadata = blob.reload()  # populates blob attributes with HEAD metadata
    return ObjectMetadataResponse(
        bucket=bucket.name,
        blob=blob.name,
        content_type=blob.content_type,
        size=blob.size,
        created=blob.time_created,
        updated=blob.time_updated,
        metadata=blob.metadata or {},
    )
