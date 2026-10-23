from typing import List
from storage_client import get_storage_client
from storage_models import S3Object


def list_objects_by_prefix(bucket: str, prefix: str) -> List[str]:
    """
    Lists objects in an S3 bucket that match a given prefix.
    """
    s3_client = get_storage_client()
    paginator = s3_client.get_paginator("list_objects_v2")
    pages = paginator.paginate(Bucket=bucket, Prefix=prefix)

    object_keys = []
    for page in pages:
        if "Contents" in page:
            for obj in page["Contents"]:
                object_keys.append(obj["Key"])

    return object_keys
