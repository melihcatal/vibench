import os
import boto3
from botocore.exceptions import ClientError
from storage_client import ManagedStorageClient


def list_objects_prefix(bucket_name: str, prefix: str, max_keys: int = 1000):
    """List objects under a bucket with the given prefix using Amazon S3.

    Args:
        bucket_name: S3 bucket name.
        prefix: Common prefix/path of objects to list.
        max_keys: Max number of keys to return in a single call.

    Returns:
        List of object summaries (dict) matching the prefix.
    """
    client = ManagedStorageClient.get_s3_client()
    try:
        paginator = client.get_paginator("list_objects_v2")
        operation_parameters = {
            "Bucket": bucket_name,
            "Prefix": prefix,
            "MaxKeys": max_keys,
        }
        page_iterator = paginator.paginate(**operation_parameters)
        objects = []
        for page in page_iterator:
            if "Contents" in page:
                objects.extend(page["Contents"])
        return objects
    except ClientError as e:
        raise RuntimeError(f"Listing objects failed: {e}")
