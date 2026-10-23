from __future__ import annotations

from typing import List, Optional

from storage_client import get_s3_client, require_bucket
from storage_models import ListedObject, normalize_s3_listing


def list_objects_with_prefix(
    bucket: str,
    prefix: str = "",
    max_keys: int = 1000,
    continuation_token: Optional[str] = None,
    region_name: Optional[str] = None,
) -> List[ListedObject]:
    s3 = get_s3_client(region_name)
    params = {
        "Bucket": require_bucket(bucket),
        "Prefix": prefix,
        "MaxKeys": max_keys,
    }
    if continuation_token:
        params["ContinuationToken"] = continuation_token
    response = s3.list_objects_v2(**params)
    return normalize_s3_listing(response.get("Contents"))
