from __future__ import annotations

from storage_client import get_s3_client
from storage_models import ListPrefixResult, ListedObject, normalize_timestamp


def list_prefix(
    bucket: str,
    prefix: str = "",
    continuation_token: str | None = None,
    max_keys: int = 1000,
) -> ListPrefixResult:
    s3 = get_s3_client("s3")
    params = {"Bucket": bucket, "Prefix": prefix, "MaxKeys": max_keys}
    if continuation_token:
        params["ContinuationToken"] = continuation_token
    response = s3.list_objects_v2(**params)
    objects = [
        ListedObject(
            key=item["Key"],
            size=item.get("Size"),
            etag=item.get("ETag"),
            last_modified=normalize_timestamp(item.get("LastModified")),
            storage_class=item.get("StorageClass"),
        )
        for item in response.get("Contents", [])
    ]
    return ListPrefixResult(
        bucket=bucket,
        prefix=prefix,
        objects=objects,
        next_continuation_token=response.get("NextContinuationToken"),
    )
