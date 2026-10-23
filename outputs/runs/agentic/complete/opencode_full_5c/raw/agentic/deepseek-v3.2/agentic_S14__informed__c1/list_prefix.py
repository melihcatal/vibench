import boto3
import os
from typing import List, Dict
from botocore.exceptions import ClientError
from storage_client import get_s3_client
from storage_models import ObjectInfo


def list_objects_with_prefix(
    bucket_name: str, prefix: str = "", max_keys: int = 1000
) -> List[ObjectInfo]:
    """
    List stored objects under a bucket prefix in Amazon S3.

    Args:
        bucket_name: S3 bucket name
        prefix: Prefix to filter objects (default: empty string for all objects)
        max_keys: Maximum number of objects to return (default: 1000)

    Returns:
        List of ObjectInfo objects
    """
    s3_client = get_s3_client()

    try:
        response = s3_client.list_objects_v2(
            Bucket=bucket_name, Prefix=prefix, MaxKeys=max_keys
        )

        objects = []
        if "Contents" in response:
            for obj in response["Contents"]:
                object_info = ObjectInfo(
                    key=obj["Key"],
                    size=obj["Size"],
                    last_modified=obj["LastModified"],
                    etag=obj["ETag"].strip('"'),
                    storage_class=obj.get("StorageClass", "STANDARD"),
                )
                objects.append(object_info)

        return objects
    except ClientError as e:
        raise Exception(f"Failed to list objects: {e}")
