import os
from typing import Dict, Optional

from boto3 import client
from botocore.exceptions import ClientError


def get_object_metadata(
    bucket_name: str,
    object_key: str,
) -> Dict[str, Optional[str]]:
    """
    Retrieves metadata or head information for an object in AWS S3.

    Args:
        bucket_name: Name of the S3 bucket.
        object_key: Key/path of the object in the bucket.

    Returns:
        Dict[str, Optional[str]]: A dictionary containing object metadata and properties.

    Raises:
        ClientError: If the metadata retrieval fails.
    """
    s3_client = client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    response = s3_client.head_object(Bucket=bucket_name, Key=object_key)

    metadata = {
        "ContentType": response.get("ContentType"),
        "ContentLength": response.get("ContentLength"),
        "ETag": response.get("ETag"),
        "LastModified": response.get("LastModified"),
        "Metadata": response.get("Metadata", {}),
    }
    return metadata
