from __future__ import annotations

from typing import Optional

from storage_client import get_s3_client
from storage_models import ListedObject, normalize_s3_list_item


def list_objects_under_prefix(
    bucket: str,
    prefix: str = "",
    max_keys: int = 1000,
    continuation_token: Optional[str] = None,
    region_name: Optional[str] = None,
) -> dict[str, object]:
    s3 = get_s3_client(region_name=region_name)
    params: dict[str, object] = {
        "Bucket": bucket,
        "Prefix": prefix,
        "MaxKeys": max_keys,
    }
    if continuation_token:
        params["ContinuationToken"] = continuation_token

    response = s3.list_objects_v2(**params)
    contents = response.get("Contents", [])
    items: list[ListedObject] = [normalize_s3_list_item(item) for item in contents]
    return {
        "items": items,
        "next_continuation_token": response.get("NextContinuationToken"),
        "is_truncated": bool(response.get("IsTruncated")),
        "bucket": bucket,
        "prefix": prefix,
    }
