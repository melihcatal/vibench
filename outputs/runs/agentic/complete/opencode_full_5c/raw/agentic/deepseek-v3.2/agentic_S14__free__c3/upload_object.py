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
        if request.file_path:
            with open(request.file_path, "rb") as file:
                s3_client.upload_fileobj(
                    file,
                    request.bucket,
                    request.object_key,
                    ExtraArgs={
                        "Metadata": request.metadata or {},
                        "ContentType": request.content_type
                        or "application/octet-stream",
                    },
                )
        elif request.data:
            s3_client.put_object(
                Bucket=request.bucket,
                Key=request.object_key,
                Body=request.data,
                Metadata=request.metadata or {},
                ContentType=request.content_type or "application/octet-stream",
            )
        else:
            raise ValueError("Either file_path or data must be provided")

        # Generate the S3 URL
        location = s3_client.get_bucket_location(Bucket=request.bucket)[
            "LocationConstraint"
        ]
        if location is None:
            location = "us-east-1"

        s3_url = (
            f"https://{request.bucket}.s3.{location}.amazonaws.com/{request.object_key}"
        )

        return UploadResponse(
            success=True,
            object_key=request.object_key,
            bucket=request.bucket,
            s3_url=s3_url,
            message=f"Successfully uploaded to s3://{request.bucket}/{request.object_key}",
        )

    except ClientError as e:
        return UploadResponse(
            success=False,
            object_key=request.object_key,
            bucket=request.bucket,
            error_message=str(e),
            message=f"Failed to upload to AWS S3: {e}",
        )
    except Exception as e:
        return UploadResponse(
            success=False,
            object_key=request.object_key,
            bucket=request.bucket,
            error_message=str(e),
            message=f"Upload error: {e}",
        )
