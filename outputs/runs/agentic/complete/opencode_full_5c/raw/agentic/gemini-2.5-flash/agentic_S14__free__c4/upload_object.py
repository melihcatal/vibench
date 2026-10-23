import os
from storage_client import StorageClient
from storage_models import UploadObjectRequest, UploadObjectResponse
from botocore.exceptions import ClientError


def upload_object(request: UploadObjectRequest) -> UploadObjectResponse:
    s3_client = StorageClient().get_s3_client()
    try:
        if request.file_path:
            with open(request.file_path, "rb") as f:
                response = s3_client.put_object(
                    Bucket=request.bucket_name,
                    Key=request.object_key,
                    Body=f,
                    ContentType=request.content_type,
                )
        elif request.data is not None:
            response = s3_client.put_object(
                Bucket=request.bucket_name,
                Key=request.object_key,
                Body=request.data,
                ContentType=request.content_type,
            )
        else:
            return UploadObjectResponse(
                success=False, message="No file_path or data provided for upload."
            )

        return UploadObjectResponse(
            success=True,
            message="Object uploaded successfully.",
            etag=response.get("ETag", "").strip('"'),
            version_id=response.get("VersionId"),
        )
    except ClientError as e:
        return UploadObjectResponse(
            success=False, message=f"Error uploading object: {e}"
        )
    except FileNotFoundError:
        return UploadObjectResponse(
            success=False, message=f"File not found at {request.file_path}"
        )
