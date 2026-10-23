import os
from typing import List

import boto3

from storage_client import get_s3_client


def list_objects_with_prefix(bucket_name: str, prefix: str) -> List[str]:
    """
    Lists objects in an S3 bucket that have a specific prefix.

    :param bucket_name: The name of the S3 bucket.
    :param prefix: The prefix to filter objects by.
    :return: A list of object keys.
    """
    s3_client = get_s3_client()
    object_keys = []
    try:
        paginator = s3_client.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)
        for page in pages:
            if "Contents" in page:
                for obj in page["Contents"]:
                    object_keys.append(obj["Key"])
    except Exception as e:
        print(f"Error listing objects with prefix '{prefix}': {e}")
    return object_keys
