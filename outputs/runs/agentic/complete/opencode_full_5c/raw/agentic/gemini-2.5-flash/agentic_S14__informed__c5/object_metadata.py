from storage_client import get_gcs_client
from storage_models import ObjectMetadataRequest, ObjectMetadataResponse


def get_object_metadata(request: ObjectMetadataRequest) -> ObjectMetadataResponse:
    client = get_gcs_client()
    bucket = client.bucket(request.bucket_name)
    blob = bucket.blob(request.object_name)

    blob.reload()

    return ObjectMetadataResponse(
        bucket_name=request.bucket_name,
        object_name=request.object_name,
        size=blob.size,
        content_type=blob.content_type if blob.content_type else "",
        e_tag=blob.etag,
        last_modified=blob.time_created.isoformat(),
        metadata=blob.metadata if blob.metadata else {},
    )
