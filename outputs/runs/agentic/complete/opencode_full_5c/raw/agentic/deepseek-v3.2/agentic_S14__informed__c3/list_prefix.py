import boto3
import os
from botocore.exceptions import ClientError
from storage_client import get_s3_client


def list_objects_with_prefix(bucket_name, prefix="", max_keys=1000):
    """
    List stored objects under a bucket or container prefix in Amazon S3.

    Args:
        bucket_name: S3 bucket name
        prefix: Prefix to filter objects (default: empty string for all objects)
        max_keys: Maximum number of objects to return (default: 1000)

    Returns:
        list: List of objects with key, size, last modified, etc.
    """
    s3_client = get_s3_client()

    try:
        paginator = s3_client.get_paginator("list_objects_v2")
        objects = []

        for page in paginator.paginate(
            Bucket=bucket_name, Prefix=prefix, PaginationConfig={"MaxItems": max_keys}
        ):
            if "Contents" in page:
                for obj in page["Contents"]:
                    objects.append(
                        {
                            "key": obj["Key"],
                            "size": obj["Size"],
                            "last_modified": obj["LastModified"].isoformat(),
                            "etag": obj["ETag"],
                            "storage_class": obj.get("StorageClass", "STANDARD"),
                        }
                    )

        return {
            "bucket": bucket_name,
            "prefix": prefix,
            "objects": objects,
            "count": len(objects),
            "provider": "Amazon S3",
        }
    except ClientError as e:
        raise Exception(f"Failed to list objects from Amazon S3: {e}")
