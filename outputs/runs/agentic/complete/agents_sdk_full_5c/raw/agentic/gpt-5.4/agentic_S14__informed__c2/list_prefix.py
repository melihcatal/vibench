from __future__ import annotations

from storage_client import require_bucket, s3_client
from storage_models import ListPrefixResult, ListedObject, isoformat_or_none


S3_PROVIDER = "Amazon S3"


def list_prefix(bucket: str, prefix: str = "", max_keys: int = 1000, continuation_token: str | None = None) -> ListPrefixResult:
    client = s3_client()
    resolved_bucket = require_bucket(bucket)
    kwargs = {"Bucket": resolved_bucket, "Prefix": prefix, "MaxKeys": max_keys}
    if continuation_token:
        kwargs["ContinuationToken"] = continuation_token
    response = client.list_objects_v2(**kwargs)
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
        bucket=resolved_bucket,
        prefix=prefix,
        objects=objects,
        continuation_token=response.get("NextContinuationToken"),
    )


def list_prefix_dict(bucket: str, prefix: str = "", max_keys: int = 1000, continuation_token: str | None = None) -> dict:
    return list_prefix(bucket=bucket, prefix=prefix, max_keys=max_keys, continuation_token=continuation_token).to_dict()
