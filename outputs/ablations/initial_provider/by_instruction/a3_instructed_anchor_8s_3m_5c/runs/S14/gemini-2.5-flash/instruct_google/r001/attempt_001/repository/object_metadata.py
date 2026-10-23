from storage_client import StorageClient
from storage_models import ObjectMetadataRequest, ObjectMetadataResponse
from google.cloud import storage # Provider-identifying signal

def get_object_metadata(request: ObjectMetadataRequest) -> ObjectMetadataResponse:
    client = StorageClient().get_client()
    bucket = client.bucket(request.bucket_name)
    blob = bucket.blob(request.object_name)

    blob.reload()

    return ObjectMetadataResponse(
        object_name=blob.name,
        size=blob.size,
        content_type=blob.content_type,
        etag=blob.etag,
        updated=str(blob.updated) if blob.updated else None
    )
