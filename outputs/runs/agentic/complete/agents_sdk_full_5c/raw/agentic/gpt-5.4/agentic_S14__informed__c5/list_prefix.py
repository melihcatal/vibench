from __future__ import annotations

from typing import Optional

from storage_client import get_s3_client
from storage_models import ListPrefixResult, normalize_s3_list_item


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
    objects = [normalize_s3_list_item(item) for item in response.get("Contents", [])]
    return ListPrefixResult(
        bucket=bucket,
        prefix=prefix,
        objects=objects,
        next_token=response.get("NextContinuationToken"),
        is_truncated=response.get("IsTruncated", False),
    )
