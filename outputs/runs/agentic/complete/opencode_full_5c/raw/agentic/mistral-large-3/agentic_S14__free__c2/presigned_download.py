import os
from datetime import timedelta

from boto3 import client
from botocore.exceptions import ClientError


def create_presigned_download_url(
    bucket_name: str,
    object_key: str,
    expiration: int = 3600,
) -> str:
    """
    Creates a time-limited signed download URL for an object in AWS S3.

    Args:
        bucket_name: Name of the S3 bucket.
        object_key: Key/path of the object in the bucket.
        expiration: Time in seconds for the URL to remain valid.

    Returns:
        str: A presigned URL for downloading the object.

    Raises:
        ClientError: If the presigned URL generation fails.
    """
    s3_client = client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    presigned_url = s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket_name, "Key": object_key},
        ExpiresIn=expiration,
    )
    return presigned_url
