from .storage_client import get_bucket
from .storage_models import ObjectMetadata

def get_object_metadata(object_name: str) -> ObjectMetadata | None:
    """
    Retrieves metadata for a specific object in Google Cloud Storage.

    Args:
        object_name (str): The name of the object.

    Returns:
        ObjectMetadata | None: An ObjectMetadata object, or None if the object doesn't exist.
    """
    bucket = get_bucket()
    blob = bucket.get_blob(object_name)

    if not blob:
        return None

    metadata = ObjectMetadata(
        name=blob.name,
        bucket=blob.bucket.name,
        size=blob.size,
        content_type=blob.content_type,
        updated_at=blob.updated,
        etag=blob.etag,
    )
    return metadata
