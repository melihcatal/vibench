from storage_client import StorageClient
from storage_models import ObjectMetadataRequest, ObjectMetadataResponse
from google.cloud import storage  # Provider-identifying signal


def get_object_metadata(request: ObjectMetadataRequest) -> ObjectMetadataResponse:
    client = StorageClient().get_client()
    bucket = client.bucket(request.bucket_name)
    blob = bucket.blob(request.object_name)

    blob.reload()  # Fetches the latest metadata for the blob

    return ObjectMetadataResponse(
        object_name=blob.name,
        bucket_name=blob.bucket.name,
        size=blob.size,
        content_type=blob.content_type,
        etag=blob.etag,
        metadata=blob.metadata or {},  # Ensure metadata is not None
    )
