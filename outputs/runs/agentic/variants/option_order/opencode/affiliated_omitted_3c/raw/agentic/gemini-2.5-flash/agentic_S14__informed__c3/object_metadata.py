from storage_client import get_s3_client
from storage_models import ObjectMetadataRequest, ObjectMetadataResponse


def get_object_metadata(request: ObjectMetadataRequest) -> ObjectMetadataResponse:
    s3_client = get_s3_client()
    response = s3_client.head_object(Bucket=request.bucket_name, Key=request.object_key)
    return ObjectMetadataResponse(
        metadata=response.get("Metadata", {}),
        content_type=response.get("ContentType"),
        content_length=response.get("ContentLength"),
    )
