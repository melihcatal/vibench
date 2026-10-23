import os
from typing import Union, BinaryIO
import boto3
from botocore.exceptions import ClientError
from storage_client import get_storage_client
from storage_models import UploadRequest, UploadResponse

def upload_object(
    request: UploadRequest
) -> UploadResponse:
    """
    Uploads a file or byte stream to AWS S3 managed object storage.
    """
    s3_client = get_storage_client()

    try:
        if isinstance(request.content, (bytes, BinaryIO)):
            s3_client.upload_fileobj(
                request.content,
                os.getenv("AWS_S3_BUCKET_NAME", "default-bucket"),
                request.object_key,
                ExtraArgs={
                    "Metadata": request.metadata or {},
                    "ContentType": request.content_type
                }
            )
        else:
            s3_client.upload_file(
                request.content,
                os.getenv("AWS_S3_BUCKET_NAME", "default-bucket"),
                request.object_key,
                ExtraArgs={
                    "Metadata": request.metadata or {},
                    "ContentType": request.content_type
                }
            )

        return UploadResponse(
            object_key=request.object_key,
            bucket_name=os.getenv("AWS_S3_BUCKET_NAME", "default-bucket"),
            success=True,
            etag=""
        )
    except ClientError as e:
        return UploadResponse(
            object_key=request.object_key,
            bucket_name=os.getenv("AWS_S3_BUCKET_NAME", "default-bucket"),
            success=False,
            error=str(e)
        )