from google.cloud import storage
from storage_client import get_storage_client, get_bucket_name
from storage_models import ObjectMetadataResponse


def get_object_metadata(object_name: str) -> ObjectMetadataResponse:
    """
    Read object metadata from Google Cloud Storage.
    """
    client = get_storage_client()
    bucket_name = get_bucket_name()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.reload()  # Ensure metadata is fresh

    return {
        "name": blob.name,
        "size": blob.size,
        "content_type": blob.content_type,
        "time_created": blob.time_created.isoformat(),
        "updated": blob.updated.isoformat(),
        "metadata": blob.metadata,
    }