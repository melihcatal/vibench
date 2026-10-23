from __future__ import annotations

from storage_client import get_bucket_name, get_s3_client
from storage_models import ListPrefixResult, ListedObject


def list_prefix(bucket: str, prefix: str, max_keys: int = 1000, continuation_token: str | None = None) -> ListPrefixResult:
    s3 = get_s3_client()
    params = {"Bucket": get_bucket_name(bucket), "Prefix": prefix, "MaxKeys": max(1, int(max_keys))}
    if continuation_token:
        params["ContinuationToken"] = continuation_token
    resp = s3.list_objects_v2(**params)
    objects = [
        ListedObject(
            key=item["Key"],
            size=item.get("Size"),
            etag=item.get("ETag"),
            last_modified=str(item.get("LastModified")) if item.get("LastModified") else None,
            storage_class=item.get("StorageClass"),
        )
        for item in resp.get("Contents", [])
    ]
    return ListPrefixResult(
        bucket=get_bucket_name(bucket),
        prefix=prefix,
        objects=objects,
        is_truncated=bool(resp.get("IsTruncated", False)),
        next_token=resp.get("NextContinuationToken"),
    )
