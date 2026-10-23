import os
from storage_client import get_s3_client
from storage_models import UploadObjectRequest, UploadObjectResponse
from botocore.exceptions import ClientError


def upload_object(request: UploadObjectRequest) -> UploadObjectResponse:
    s3_client = get_s3_client()
    try:
        if request.file_path:
            if not os.path.exists(request.file_path):
                return UploadObjectResponse(
                    success=False, message=f"File not found: {request.file_path}"
                )
            extra_args = (
                {"ContentType": request.content_type} if request.content_type else {}
            )
            s3_client.upload_file(
                request.file_path,
                request.bucket_name,
                request.object_key,
                ExtraArgs=extra_args,
            )
        elif request.data:
            extra_args = (
                {"ContentType": request.content_type} if request.content_type else {}
            )
            s3_client.put_object(
                Bucket=request.bucket_name,
                Key=request.object_key,
                Body=request.data,
                **extra_args,
            )
        else:
            return UploadObjectResponse(
                success=False, message="Either file_path or data must be provided."
            )

        object_url = f"https://{request.bucket_name}.s3.{s3_client.meta.region_name}.amazonaws.com/{request.object_key}"
        return UploadObjectResponse(
            success=True, message="Object uploaded successfully", object_url=object_url
        )
    except ClientError as e:
        return UploadObjectResponse(success=False, message=f"AWS S3 ClientError: {e}")
    except Exception as e:
        return UploadObjectResponse(
            success=False, message=f"An unexpected error occurred: {e}"
        )
