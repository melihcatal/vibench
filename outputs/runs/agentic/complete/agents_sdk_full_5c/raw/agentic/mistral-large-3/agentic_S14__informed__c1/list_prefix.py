from typing import List

from storage_client import get_storage_client, get_bucket_name
from storage_models import ObjectMetadata


def list_objects_with_prefix(prefix: str, max_keys: int = 1000) -> List[ObjectMetadata]:
    """
    List objects under a prefix in Amazon S3.
    """
    client = get_storage_client()
    bucket = get_bucket_name()

    paginator = client.get_paginator("list_objects_v2")
    page_iterator = paginator.paginate(Bucket=bucket, Prefix=prefix, PaginationConfig={"MaxItems": max_keys})

    objects = []
    for page in page_iterator:
        if "Contents" in page:
            for obj in page["Contents"]:
                objects.append(
                    ObjectMetadata(
                        key=obj["Key"],
                        size=obj["Size"],
                        etag=obj["ETag"].strip('"'),
                        last_modified=obj["LastModified"].isoformat(),
                        storage_class=obj["StorageClass"],
                    )
                )

    return objects