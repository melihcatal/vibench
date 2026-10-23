from __future__ import annotations

from storage_client import get_s3_client
from storage_models import ListPrefixResult, ListedObject, isoformat_or_none


def list_prefix(
    bucket: str,
    prefix: str = "",
    continuation_token: str | None = None,
    max_keys: int = 1000,
) -> ListPrefixResult:
    client = get_s3_client()
    params: dict[str, object] = {
        "Bucket": bucket,
        "Prefix": prefix,
        "MaxKeys": max_keys,
    }
    if continuation_token:
        params["ContinuationToken"] = continuation_token
    response = client.list_objects_v2(**params)
    objects = [
        ListedObject(
            key=item["Key"],
            size=item.get("Size"),
            etag=item.get("ETag"),
            last_modified=isoformat_or_none(item.get("LastModified")),
            storage_class=item.get("StorageClass"),
        )
        for item in response.get("Contents", [])
    ]
    return ListPrefixResult(
        bucket=bucket,
        prefix=prefix,
        objects=objects,
        next_token=response.get("NextContinuationToken"),
        is_truncated=bool(response.get("IsTruncated")),
    )
