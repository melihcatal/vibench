import os
from storage_client import get_s3_client
from storage_models import UploadObjectRequest, UploadObjectResponse


def upload_object(request: UploadObjectRequest) -> UploadObjectResponse:
    s3_client = get_s3_client()

    if request.file_path:
        with open(request.file_path, "rb") as f:
            response = s3_client.put_object(
                Bucket=request.bucket_name,
                Key=request.object_name,
                Body=f,
                ContentType=request.content_type,
            )
    elif request.data:
        response = s3_client.put_object(
            Bucket=request.bucket_name,
            Key=request.object_name,
            Body=request.data,
            ContentType=request.content_type,
        )
    else:
        raise ValueError("Either file_path or data must be provided for upload.")

    return UploadObjectResponse(
        e_tag=response["ETag"].strip('"'), version_id=response.get("VersionId")
    )
