from storage_client import get_s3_client
from storage_models import ListObjectsResult


def list_objects_with_prefix(bucket_name: str, prefix: str = "", config: dict = None) -> ListObjectsResult:
    config = config or {}
    s3_client = get_s3_client(region_name=config.get("region"))
    object_names = []
    paginator = s3_client.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)
    for page in pages:
        if "Contents" in page:
            for obj in page["Contents"]:
                object_names.append(obj["Key"])
    return ListObjectsResult(object_names=object_names)
