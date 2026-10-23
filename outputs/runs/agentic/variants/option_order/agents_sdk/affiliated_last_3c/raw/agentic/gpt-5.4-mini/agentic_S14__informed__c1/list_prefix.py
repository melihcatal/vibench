from __future__ import annotations

from typing import List

from storage_client import resolve_key, s3_client
from storage_models import ListedObject


def list_objects(bucket: str, prefix: str = "", max_items: int | None = None) -> List[ListedObject]:
    client = s3_client()
    resolved_prefix = resolve_key(prefix) if prefix else ""
    paginator = client.get_paginator("list_objects_v2")
    pagination_kwargs = {"Bucket": bucket, "Prefix": resolved_prefix}
    results: List[ListedObject] = []
    for page in paginator.paginate(**pagination_kwargs):
        for item in page.get("Contents", []):
            results.append(
                ListedObject(
                    key=item["Key"],
                    size=item.get("Size", 0),
                    last_modified=str(item.get("LastModified")) if item.get("LastModified") else None,
                    etag=item.get("ETag"),
                    storage_class=item.get("StorageClass"),
                )
            )
            if max_items is not None and len(results) >= max_items:
                return results
    return results
