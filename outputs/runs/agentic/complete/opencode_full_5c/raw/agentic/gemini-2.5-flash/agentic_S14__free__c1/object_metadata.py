from storage_client import get_storage_client
from storage_models import ObjectMetadataRequest, ObjectMetadata


def get_object_metadata(request: ObjectMetadataRequest) -> ObjectMetadata:
    client = get_storage_client()
    bucket = client.bucket(request.bucket_name)
    blob = bucket.get_blob(request.object_name)
    if not blob:
        raise ValueError(
            f"Object {request.object_name} not found in bucket {request.bucket_name}"
        )

    return ObjectMetadata(
        name=blob.name,
        size=blob.size,
        content_type=blob.content_type,
        etag=blob.etag,
        custom_metadata=blob.metadata,
    )
