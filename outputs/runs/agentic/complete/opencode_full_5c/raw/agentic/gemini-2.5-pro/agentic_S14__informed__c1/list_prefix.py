from storage_client import get_storage_client
from typing import List


def list_objects_by_prefix(bucket_name: str, prefix: str) -> List[str]:
    """
    Lists object keys in an S3 bucket that match a given prefix.

    :param bucket_name: The name of the S3 bucket.
    :param prefix: The prefix to filter objects by.
    :return: A list of object keys.
    """
    s3_client = get_storage_client()
    paginator = s3_client.get_paginator("list_objects_v2")
    pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

    object_keys = []
    for page in pages:
        if "Contents" in page:
            for obj in page["Contents"]:
                object_keys.append(obj["Key"])

    return object_keys
