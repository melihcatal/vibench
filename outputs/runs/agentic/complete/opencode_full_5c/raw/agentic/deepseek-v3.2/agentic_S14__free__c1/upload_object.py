import boto3
from botocore.exceptions import ClientError
import os
from storage_client import get_s3_client
from storage_models import UploadRequest, UploadResponse


def upload_object(request: UploadRequest) -> UploadResponse:
    """Upload a file or byte stream to AWS S3 managed object storage."""
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

        # Get the uploaded object URL
        location = s3_client.get_bucket_location(Bucket=request.bucket)[
            "LocationConstraint"
        ]
        region = "" if location is None else f"{location}."
        object_url = (
            f"https://{request.bucket}.s3.{region}amazonaws.com/{request.object_key}"
        )

        return UploadResponse(
            success=True,
            object_url=object_url,
            bucket=request.bucket,
            object_key=request.object_key,
            message="Object uploaded successfully",
        )

    except ClientError as e:
        return UploadResponse(success=False, error_message=f"AWS S3 error: {str(e)}")
    except Exception as e:
        return UploadResponse(success=False, error_message=f"Upload failed: {str(e)}")
