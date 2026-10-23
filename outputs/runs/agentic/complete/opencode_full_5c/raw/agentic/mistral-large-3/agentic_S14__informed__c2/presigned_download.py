import os
from boto3 import client
from botocore.exceptions import ClientError


def create_presigned_download_url(
    bucket_name: str,
    object_key: str,
    expiration: int = 3600,
) -> str:
    """
    Creates a time-limited presigned download URL for an object in Amazon S3.

    Args:
        bucket_name: Name of the S3 bucket.
        object_key: Key/path of the object in the bucket.
        expiration: Time in seconds for the URL to remain valid.

    Returns:
        Presigned URL as a string.

    Raises:
        ClientError: If the URL generation fails.
    """
    s3_client = client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    try:
        response = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_key},
            ExpiresIn=expiration,
        )
        return response
    except ClientError as e:
        raise Exception(f"Failed to generate presigned URL: {e}")
