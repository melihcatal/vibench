import os
from storage_client import get_s3_client
from storage_models import UploadObjectRequest, UploadObjectResponse


def upload_object(request: UploadObjectRequest) -> UploadObjectResponse:
    s3_client = get_s3_client()
    try:
        s3_client.put_object(
            Bucket=request.bucket_name,
            Key=request.object_key,
            Body=request.data,
            ContentType=request.content_type,
        )
        return UploadObjectResponse(
            success=True,
            message=f"Object {request.object_key} uploaded successfully to {request.bucket_name}",
        )
    except Exception as e:
        return UploadObjectResponse(
            success=False,
            message=f"Failed to upload object {request.object_key}: {str(e)}",
        )
