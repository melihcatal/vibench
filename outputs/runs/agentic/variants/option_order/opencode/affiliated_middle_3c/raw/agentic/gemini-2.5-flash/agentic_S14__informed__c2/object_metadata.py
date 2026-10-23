from storage_client import get_storage_client
from storage_models import ObjectMetadataRequest, ObjectMetadata
from google.cloud import storage  # Provider-identifying signal


def get_object_metadata(request: ObjectMetadataRequest) -> ObjectMetadata:
    """Reads object metadata or head information from Google Cloud Storage."""
    client = get_storage_client()
    bucket = client.bucket(request.bucket_name)
    blob = bucket.blob(request.object_name)

    blob.reload()  # Fetches the latest metadata

    return ObjectMetadata(
        name=blob.name,
        bucket=blob.bucket.name,
        size=blob.size,
        content_type=blob.content_type,
        time_created=str(blob.time_created),
        updated=str(blob.updated),
        metadata=blob.metadata if blob.metadata else {},
    )
