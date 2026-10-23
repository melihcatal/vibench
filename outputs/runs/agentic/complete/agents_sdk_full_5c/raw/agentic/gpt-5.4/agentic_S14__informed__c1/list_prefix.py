from __future__ import annotations

from typing import Optional

from storage_client import get_s3_client
from storage_models import ListPrefixResult, ListedObject


def list_objects_with_prefix(
    bucket: str,
    prefix: str = "",
    max_keys: int = 1000,
    continuation_token: Optional[str] = None,
    region_name: Optional[str] = None,
) -> ListPrefixResult:
    s3 = get_s3_client(region_name=region_name)
    params = {"Bucket": bucket, "Prefix": prefix, "MaxKeys": max_keys}
    if continuation_token:
        params["ContinuationToken"] = continuation_token
    response = s3.list_objects_v2(**params)
    objects = [
        ListedObject(
            key=item["Key"],
            size=item.get("Size"),
            etag=item.get("ETag"),
            last_modified=item.get("LastModified"),
            storage_class=item.get("StorageClass"),
        )
        for item in response.get("Contents", [])
    ]
    return ListPrefixResult(
        bucket=bucket,
        prefix=prefix,
        objects=objects,
        is_truncated=response.get("IsTruncated", False),
        next_token=response.get("NextContinuationToken"),
    )
