from __future__ import annotations

from storage_client import get_s3_client
from storage_models import ListPrefixResult, ListedObject


def list_objects_with_prefix(
    bucket_name: str,
    prefix: str,
    continuation_token: str | None = None,
    max_keys: int = 1000,
) -> ListPrefixResult:
    s3_client = get_s3_client()
    params = {"Bucket": bucket_name, "Prefix": prefix, "MaxKeys": max_keys}
    if continuation_token:
        params["ContinuationToken"] = continuation_token
    response = s3_client.list_objects_v2(**params)
    objects = [
        ListedObject(
            object_name=item["Key"],
            size=item.get("Size"),
            etag=(item.get("ETag") or "").strip('"') or None,
            last_modified=item.get("LastModified"),
            storage_class=item.get("StorageClass"),
        )
        for item in response.get("Contents", [])
    ]
    return ListPrefixResult(
        bucket_name=bucket_name,
        prefix=prefix,
        objects=objects,
        next_continuation_token=response.get("NextContinuationToken"),
    )
