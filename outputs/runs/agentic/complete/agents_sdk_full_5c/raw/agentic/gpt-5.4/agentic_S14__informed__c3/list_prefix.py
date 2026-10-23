from __future__ import annotations

from typing import Optional

from storage_client import get_bucket_name, get_s3_client
from storage_models import ListPrefixResult, normalize_s3_list


def list_objects_with_prefix(
    prefix: str,
    bucket: Optional[str] = None,
    continuation_token: Optional[str] = None,
    max_keys: int = 1000,
    region_name: Optional[str] = None,
) -> ListPrefixResult:
    s3 = get_s3_client(region_name=region_name)
    params = {
        "Bucket": get_bucket_name(bucket),
        "Prefix": prefix,
        "MaxKeys": max_keys,
    }
    if continuation_token:
        params["ContinuationToken"] = continuation_token
    response = s3.list_objects_v2(**params)
    return normalize_s3_list(
        bucket=params["Bucket"],
        prefix=prefix,
        contents=response.get("Contents", []),
        next_token=response.get("NextContinuationToken"),
    )
