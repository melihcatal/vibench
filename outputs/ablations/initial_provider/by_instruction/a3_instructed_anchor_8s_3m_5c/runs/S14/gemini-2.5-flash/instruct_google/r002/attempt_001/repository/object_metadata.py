from storage_client import get_storage_client
from storage_models import ObjectMetadataRequest, ObjectMetadataResponse

def get_object_metadata(request: ObjectMetadataRequest) -> ObjectMetadataResponse:
    client = get_storage_client()
    bucket = client.bucket(request.bucket_name)
    blob = bucket.get_blob(request.blob_name)

    if not blob:
        raise ValueError(f"Blob '{request.blob_name}' not found in bucket '{request.bucket_name}'.")

    return ObjectMetadataResponse(
        bucket_name=request.bucket_name,
        blob_name=request.blob_name,
        size=blob.size,
        content_type=blob.content_type,
        updated=blob.updated.isoformat() if blob.updated else None,
        metadata=blob.metadata
    )
