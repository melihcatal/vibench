from storage_client import get_storage_client
from storage_models import ObjectMetadataResponse

def get_object_metadata(bucket_name: str, object_key: str) -> ObjectMetadataResponse:
    """
    Reads object metadata from Google Cloud Storage.
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable.
    """
    client = get_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_key)
    blob.reload()  # Ensure metadata is fresh

    return ObjectMetadataResponse(
        bucket=bucket_name,
        object_key=object_key,
        size=blob.size,
        content_type=blob.content_type,
        etag=blob.etag,
        last_modified=blob.updated,
        metadata=blob.metadata or {}
    )