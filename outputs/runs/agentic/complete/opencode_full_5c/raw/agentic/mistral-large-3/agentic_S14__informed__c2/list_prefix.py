import os
from boto3 import client
from botocore.exceptions import ClientError
from typing import List, Dict


def list_objects_under_prefix(
    bucket_name: str,
    prefix: str = "",
    max_keys: int = 1000,
) -> List[Dict[str, str]]:
    """
    Lists objects under a prefix in an Amazon S3 bucket.

    Args:
        bucket_name: Name of the S3 bucket.
        prefix: Prefix to filter objects (e.g., "folder/").
        max_keys: Maximum number of objects to return.

    Returns:
        List of dictionaries, each containing object details (e.g., Key, Size, LastModified).

    Raises:
        ClientError: If the listing fails.
    """
    s3_client = client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    try:
        response = s3_client.list_objects_v2(
            Bucket=bucket_name,
            Prefix=prefix,
            MaxKeys=max_keys,
        )

        objects = []
        if "Contents" in response:
            for obj in response["Contents"]:
                objects.append(
                    {
                        "Key": obj.get("Key"),
                        "Size": obj.get("Size"),
                        "LastModified": obj.get("LastModified"),
                        "ETag": obj.get("ETag"),
                    }
                )
        return objects
    except ClientError as e:
        raise Exception(f"Failed to list objects: {e}")
