from storage_client import get_s3_client
from storage_models import ObjectUploadRequest, ObjectUploadResponse


def upload_object(request: ObjectUploadRequest) -> ObjectUploadResponse:
    s3_client = get_s3_client()
    response = s3_client.put_object(
        Bucket=request.bucket_name,
        Key=request.object_key,
        Body=request.data,
        Metadata=request.metadata,
    )
    return ObjectUploadResponse(
        e_tag=response["ETag"].strip('"'),  # Remove quotes from ETag
        version_id=response.get("VersionId"),
    )
