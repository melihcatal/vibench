from __future__ import annotations

from typing import List

from storage_client import get_bucket_name, get_s3_client
from storage_models import ListedObject, normalize_datetime


def list_prefix(prefix: str = "", max_keys: int = 1000) -> List[ListedObject]:
    s3 = get_s3_client()
    response = s3.list_objects_v2(Bucket=get_bucket_name(), Prefix=prefix, MaxKeys=max_keys)
    results: List[ListedObject] = []
    for item in response.get("Contents", []):
        results.append(
            ListedObject(
                bucket=get_bucket_name(),
                key=item["Key"],
                size=item.get("Size"),
                last_modified=normalize_datetime(item.get("LastModified")),
                etag=item.get("ETag"),
            )
        )
    return results
