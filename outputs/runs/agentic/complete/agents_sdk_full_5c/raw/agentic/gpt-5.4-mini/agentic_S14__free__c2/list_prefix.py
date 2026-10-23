from __future__ import annotations

from typing import Optional

from storage_client import get_s3_client, load_storage_config
from storage_models import ListedObject, ListingResult


def list_prefix(bucket: Optional[str], prefix: str = "", max_keys: int = 1000, continuation_token: Optional[str] = None) -> ListingResult:
    client = get_s3_client()
    resolved_bucket = bucket or load_storage_config().bucket
    if not resolved_bucket:
        raise ValueError("bucket is required")

    params = {"Bucket": resolved_bucket, "Prefix": prefix, "MaxKeys": max_keys}
    if continuation_token:
        params["ContinuationToken"] = continuation_token

    response = client.list_objects_v2(**params)
    objects = [
        ListedObject(
            key=item["Key"],
            size=item.get("Size", 0),
            last_modified=item.get("LastModified").isoformat() if item.get("LastModified") else None,
            etag=item.get("ETag"),
        )
        for item in response.get("Contents", [])
    ]
    return ListingResult(
        bucket=resolved_bucket,
        prefix=prefix,
        objects=objects,
        next_token=response.get("NextContinuationToken"),
    )
