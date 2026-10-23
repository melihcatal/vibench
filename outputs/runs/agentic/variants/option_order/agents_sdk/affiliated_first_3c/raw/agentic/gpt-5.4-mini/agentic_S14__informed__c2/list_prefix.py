from __future__ import annotations

from typing import Optional

from storage_client import get_s3_client, resolve_bucket
from storage_models import ListedObject, ListPrefixResponse, isoformat_utc


def list_prefix(bucket: Optional[str], prefix: str = "", max_keys: int = 1000) -> dict:
    resolved_bucket = resolve_bucket(bucket)
    client = get_s3_client()
    response = client.list_objects_v2(Bucket=resolved_bucket, Prefix=prefix, MaxKeys=max_keys)
    objects = []
    for item in response.get("Contents", []):
        objects.append(
            ListedObject(
                key=item["Key"],
                size=item.get("Size"),
                last_modified=isoformat_utc(item.get("LastModified")),
                etag=item.get("ETag"),
            )
        )
    model = ListPrefixResponse(bucket=resolved_bucket, prefix=prefix, objects=objects)
    return {
        "bucket": model.bucket,
        "prefix": model.prefix,
        "objects": [obj.__dict__ for obj in model.objects],
        "is_truncated": response.get("IsTruncated", False),
        "key_count": response.get("KeyCount", len(model.objects)),
    }
