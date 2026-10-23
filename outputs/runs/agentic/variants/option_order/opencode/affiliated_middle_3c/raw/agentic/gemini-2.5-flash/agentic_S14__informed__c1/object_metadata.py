from storage_client import get_storage_client
from storage_models import ObjectMetadataRequest, ObjectMetadataResponse


def get_object_metadata(request: ObjectMetadataRequest) -> ObjectMetadataResponse:
    """
    Reads object metadata or head information from Google Cloud Storage.
    """
    client = get_storage_client()
    bucket = client.bucket(request.bucket_name)
    blob = bucket.blob(request.object_name)
    blob.reload()  # Fetches the latest metadata

    return ObjectMetadataResponse(
        bucket_name=request.bucket_name,
        object_name=request.object_name,
        size=blob.size,
        content_type=blob.content_type,
        e_tag=blob.etag,
        metadata=blob.metadata if blob.metadata else {},
    )
