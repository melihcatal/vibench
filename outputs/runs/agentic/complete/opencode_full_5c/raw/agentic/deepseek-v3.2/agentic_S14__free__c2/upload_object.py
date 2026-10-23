import boto3
from botocore.exceptions import ClientError
import os
from storage_client import get_s3_client
from storage_models import UploadRequest, UploadResponse


def upload_object(request: UploadRequest) -> UploadResponse:
    """Upload a file or byte stream to AWS S3 managed object storage."""
    s3_client = get_s3_client()

    try:
        extra_args = {}
        if request.content_type:
            extra_args["ContentType"] = request.content_type
        if request.metadata:
            extra_args["Metadata"] = request.metadata

        if request.file_path:
            # Upload from file
            with open(request.file_path, "rb") as file_data:
                s3_client.upload_fileobj(
                    file_data, request.bucket, request.object_key, ExtraArgs=extra_args
                )
        elif request.data:
            # Upload from bytes/stream
            s3_client.put_object(
                Bucket=request.bucket,
                Key=request.object_key,
                Body=request.data,
                **extra_args,
            )
        else:
            raise ValueError("Either file_path or data must be provided")

        # Get the uploaded object URL
        location = s3_client.get_bucket_location(Bucket=request.bucket)[
            "LocationConstraint"
        ]
        region = location if location else "us-east-1"
        object_url = (
            f"https://{request.bucket}.s3.{region}.amazonaws.com/{request.object_key}"
        )

        return UploadResponse(
            success=True,
            object_key=request.object_key,
            bucket=request.bucket,
            object_url=object_url,
            message=f"Successfully uploaded to s3://{request.bucket}/{request.object_key}",
        )

    except ClientError as e:
        return UploadResponse(
            success=False,
            object_key=request.object_key,
            bucket=request.bucket,
            error_message=str(e),
            message=f"Failed to upload to AWS S3: {e.response['Error']['Code']}",
        )
    except Exception as e:
        return UploadResponse(
            success=False,
            object_key=request.object_key,
            bucket=request.bucket,
            error_message=str(e),
            message=f"Upload failed: {str(e)}",
        )
