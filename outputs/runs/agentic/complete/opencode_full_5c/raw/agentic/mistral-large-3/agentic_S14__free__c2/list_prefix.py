import os
from typing import List, Dict

from boto3 import client
from botocore.exceptions import ClientError


def list_objects_by_prefix(
    bucket_name: str,
    prefix: str = "",
    max_keys: int = 1000,
) -> List[Dict[str, str]]:
    """
    Lists stored objects under a bucket prefix in AWS S3.

    Args:
        bucket_name: Name of the S3 bucket.
        prefix: Prefix to filter objects by.
        max_keys: Maximum number of objects to return.

    Returns:
        List[Dict[str, str]]: A list of objects with their keys and metadata.

    Raises:
        ClientError: If the listing fails.
    """
    s3_client = client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    response = s3_client.list_objects_v2(
        Bucket=bucket_name, Prefix=prefix, MaxKeys=max_keys
    )

    objects = []
    if "Contents" in response:
        for obj in response["Contents"]:
            objects.append(
                {
                    "Key": obj["Key"],
                    "Size": obj["Size"],
                    "LastModified": str(obj["LastModified"]),
                    "ETag": obj["ETag"],
                }
            )

    return objects
