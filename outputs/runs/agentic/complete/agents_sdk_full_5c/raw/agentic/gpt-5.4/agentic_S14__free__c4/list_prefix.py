from __future__ import annotations

from storage_client import get_s3_client
from storage_models import ListedObject, normalize_s3_list_item


def list_objects_with_prefix(bucket: str, prefix: str, max_keys: int = 1000) -> list[ListedObject]:
    s3 = get_s3_client()
    paginator = s3.get_paginator("list_objects_v2")
    page_iterator = paginator.paginate(Bucket=bucket, Prefix=prefix, PaginationConfig={"PageSize": max_keys})

    results: list[ListedObject] = []
    for page in page_iterator:
        for item in page.get("Contents", []):
            results.append(normalize_s3_list_item(item))
    return results
