from storage_client import get_storage_client
from storage_models import ObjectMetadataRequest, ObjectMetadataResponse

def get_object_metadata(
    request: ObjectMetadataRequest
) -> ObjectMetadataResponse:
    """Reads object metadata from Google Cloud Storage."""
    client = get_storage_client()
    bucket = client.bucket(request.bucket_name)
    blob = bucket.blob(request.object_name)

    # Fetch the blob's metadata without downloading its content
    blob.reload()

    return ObjectMetadataResponse(
        bucket_name=request.bucket_name,
        object_name=request.object_name,
        size=blob.size,
        content_type=blob.content_type,
        md5_hash=blob.md5_hash,
        crc32c_hash=blob.crc32c,
        etag=blob.etag,
        time_created=blob.time_created.isoformat() if blob.time_created else None,
        updated=blob.updated.isoformat() if blob.updated else None,
        metadata=blob.metadata # Custom metadata if any
    )
