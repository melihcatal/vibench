import boto3
from botocore.exceptions import ClientError
import os
from storage_client import get_s3_client
from storage_models import UploadRequest, UploadResponse


def upload_object(request: UploadRequest) -> UploadResponse:
    """
    Uploads a file or byte stream to AWS S3 managed object storage.
    """
    s3_client = get_s3_client()

    try:
        # Check if we're uploading from file path or bytes
        if request.file_path:
            with open(request.file_path, "rb") as file:
                file_data = file.read()
        elif request.data:
            file_data = request.data
        else:
            raise ValueError("Either file_path or data must be provided")

        # Upload to S3
        extra_args = {}
        if request.content_type:
            extra_args["ContentType"] = request.content_type
        if request.metadata:
            extra_args["Metadata"] = request.metadata

        s3_client.put_object(
            Bucket=request.bucket, Key=request.key, Body=file_data, **extra_args
        )

        # Generate the S3 URL
        s3_url = f"https://{request.bucket}.s3.amazonaws.com/{request.key}"

        return UploadResponse(
            success=True,
            bucket=request.bucket,
            key=request.key,
            url=s3_url,
            message=f"Successfully uploaded to s3://{request.bucket}/{request.key}",
        )

    except ClientError as e:
        return UploadResponse(
            success=False,
            bucket=request.bucket,
            key=request.key,
            error_message=f"S3 upload error: {str(e)}",
        )
    except Exception as e:
        return UploadResponse(
            success=False,
            bucket=request.bucket,
            key=request.key,
            error_message=f"Upload error: {str(e)}",
        )
