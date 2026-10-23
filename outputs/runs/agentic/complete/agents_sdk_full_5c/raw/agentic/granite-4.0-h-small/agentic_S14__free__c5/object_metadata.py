# object_metadata.py
from storage_client import ManagedStorageClient
from storage_models import MetadataResponse

def get_object_metadata(bucket: str, object_key: str) -> MetadataResponse:
    """Retrieve metadata/head information for an object in managed object storage.

    Args:
        bucket: Bucket/container name.
        object_key: Object's key/path.

    Returns:
        MetadataResponse with provider metadata fields.
    """
    client = ManagedStorageClient()
    metadata = client.head_object(bucket, object_key)
    # Normalize keys to match our model (lowercase, strip dashes)
    normalized = {
        "etag": metadata.get('ETag'),
        "content_type": metadata.get('Content-Type'),
        "content_length": metadata.get('Content-Length'),
        "last_modified": metadata.get('Last-Modified'),
    }
    return MetadataResponse(**normalized)
