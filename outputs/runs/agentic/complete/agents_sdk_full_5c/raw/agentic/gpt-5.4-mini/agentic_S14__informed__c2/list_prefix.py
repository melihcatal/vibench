from __future__ import annotations

from typing import Any, Dict, List

from storage_client import get_s3_client, load_storage_config
from storage_models import ListPrefixRequest, ListedObject


def list_objects_under_prefix(bucket: str, prefix: str = "", max_items: int | None = None) -> Dict[str, Any]:
    config = load_storage_config(bucket)
    client = get_s3_client(config)
    request = ListPrefixRequest(bucket=bucket, prefix=prefix, max_items=max_items)
    kwargs: Dict[str, Any] = {"Bucket": request.bucket, "Prefix": request.prefix}
    if request.max_items is not None:
        kwargs["MaxKeys"] = request.max_items
    response = client.list_objects_v2(**kwargs)
    items: List[Dict[str, Any]] = []
    for obj in response.get("Contents", []):
        item = ListedObject(
            bucket=request.bucket,
            key=obj.get("Key", ""),
            size=obj.get("Size"),
            last_modified=str(obj.get("LastModified")) if obj.get("LastModified") else None,
            etag=obj.get("ETag"),
            storage_class=obj.get("StorageClass"),
        )
        items.append({
            "bucket": item.bucket,
            "key": item.key,
            "size": item.size,
            "last_modified": item.last_modified,
            "etag": item.etag,
            "storage_class": item.storage_class,
        })
    return {
        "bucket": request.bucket,
        "prefix": request.prefix,
        "truncated": response.get("IsTruncated", False),
        "next_continuation_token": response.get("NextContinuationToken"),
        "objects": items,
    }
