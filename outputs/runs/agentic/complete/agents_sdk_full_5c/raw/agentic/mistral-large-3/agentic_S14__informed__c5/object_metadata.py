from google.cloud import storage
from storage_client import get_storage_client
from storage_models import ObjectMetadataRequest, ObjectMetadataResponse

def get_object_metadata(request: ObjectMetadataRequest) -> ObjectMetadataResponse:
    """Retrieve metadata for a Google Cloud Storage object."""
    client = get_storage_client()
    bucket = client.bucket(request.bucket_name)
    blob = bucket.blob(request.object_key)
    blob.reload()  # Ensure metadata is fetched

    return ObjectMetadataResponse(
        bucket_name=request.bucket_name,
        object_key=request.object_key,
        content_type=blob.content_type,
        size=blob.size,
        etag=blob.etag,
        last_modified=blob.updated,
        metadata=blob.metadata or {}
    )