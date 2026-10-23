import os
from boto3 import client
from botocore.exceptions import ClientError
from typing import Dict, Optional


def get_object_metadata(
    bucket_name: str,
    object_key: str,
) -> Dict[str, Optional[str]]:
    """
    Retrieves metadata and head information for an object in Amazon S3.

    Args:
        bucket_name: Name of the S3 bucket.
        object_key: Key/path of the object in the bucket.

    Returns:
        Dictionary containing metadata and head information (e.g., ContentType, ETag, Size).

    Raises:
        ClientError: If the metadata retrieval fails.
    """
    s3_client = client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    try:
        response = s3_client.head_object(
            Bucket=bucket_name,
            Key=object_key,
        )
        return {
            "ContentType": response.get("ContentType"),
            "ETag": response.get("ETag"),
            "ContentLength": response.get("ContentLength"),
            "LastModified": response.get("LastModified"),
            "Metadata": response.get("Metadata", {}),
        }
    except ClientError as e:
        raise Exception(f"Failed to retrieve object metadata: {e}")
