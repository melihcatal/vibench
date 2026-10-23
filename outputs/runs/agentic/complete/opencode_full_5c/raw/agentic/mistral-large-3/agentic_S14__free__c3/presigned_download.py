import os
from datetime import datetime, timedelta

from boto3 import client
from botocore.exceptions import ClientError

from storage_client import get_storage_client
from storage_models import PresignedDownloadResponse


def create_presigned_download_url(
    bucket_name: str,
    object_key: str,
    expires_in: int = 3600,
) -> PresignedDownloadResponse:
    """
    Creates a time-limited presigned download URL for an object in AWS S3.

    Args:
        bucket_name: Name of the S3 bucket.
        object_key: Key/path of the object in the bucket.
        expires_in: Time in seconds until the URL expires (default: 3600).

    Returns:
        PresignedDownloadResponse containing the presigned URL and expiry time.

    Raises:
        ClientError: If the presigned URL generation fails.
    """
    s3_client = get_storage_client()

    try:
        url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_key},
            ExpiresIn=expires_in,
        )
        expiry_time = datetime.utcnow() + timedelta(seconds=expires_in)

        return PresignedDownloadResponse(url=url, expiry_time=expiry_time)
    except ClientError as e:
        raise ClientError(
            error_response={
                "Error": {
                    "Code": e.response["Error"]["Code"],
                    "Message": e.response["Error"]["Message"],
                }
            },
            operation_name="create_presigned_download_url",
        )
