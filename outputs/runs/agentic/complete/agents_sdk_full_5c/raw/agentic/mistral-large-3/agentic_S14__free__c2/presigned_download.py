import os
from datetime import timedelta
import boto3
from botocore.exceptions import ClientError
from storage_client import get_storage_client
from storage_models import PresignedDownloadRequest, PresignedDownloadResponse

def create_presigned_download_url(
    request: PresignedDownloadRequest
) -> PresignedDownloadResponse:
    """
    Creates a time-limited signed download URL for an object in AWS S3.
    """
    s3_client = get_storage_client()

    try:
        url = s3_client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": os.getenv("AWS_S3_BUCKET_NAME", "default-bucket"),
                "Key": request.object_key
            },
            ExpiresIn=int(timedelta(minutes=request.expiry_minutes).total_seconds())
        )

        return PresignedDownloadResponse(
            download_url=url,
            object_key=request.object_key,
            expiry_minutes=request.expiry_minutes,
            success=True
        )
    except ClientError as e:
        return PresignedDownloadResponse(
            download_url="",
            object_key=request.object_key,
            expiry_minutes=request.expiry_minutes,
            success=False,
            error=str(e)
        )