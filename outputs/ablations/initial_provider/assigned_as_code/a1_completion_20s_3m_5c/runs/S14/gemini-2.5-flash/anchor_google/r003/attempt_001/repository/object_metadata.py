from google.cloud import storage
from storage_client import get_storage_client
from storage_models import ObjectMetadataRequest, ObjectMetadataResponse

def get_object_metadata(payload: ObjectMetadataRequest, config=None):
    config = config or {}
    client = get_storage_client(config["project_id"])
    bucket = client.bucket(payload.bucket_name)
    blob = bucket.blob(payload.object_name)

    blob.reload()

    return ObjectMetadataResponse(
        object_name=blob.name,
        bucket_name=blob.bucket.name,
        size=blob.size,
        content_type=blob.content_type,
        etag=blob.etag,
        updated=blob.updated.isoformat(),
    )
