from storage_client import get_s3_client
from storage_models import ListResponse, normalize_list_keys


def list_prefix(bucket: str, prefix: str = "") -> ListResponse:
    client = get_s3_client()
    paginator = client.get_paginator("list_objects_v2")
    items = []
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        items.extend(page.get("Contents", []))
    return normalize_list_keys(bucket, prefix, items)
