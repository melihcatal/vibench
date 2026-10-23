from __future__ import annotations

from typing import Optional

from storage_client import build_s3_client, require_bucket
from storage_models import ListPrefixResult, normalize_s3_list


def list_prefix(
    bucket: str,
    prefix: str,
    continuation_token: Optional[str] = None,
    max_keys: int = 1000,
) -> ListPrefixResult:
    s3 = build_s3_client()
    bucket_name = require_bucket(bucket)
    params = {
        "Bucket": bucket_name,
        "Prefix": prefix,
        "MaxKeys": max_keys,
    }
    if continuation_token:
        params["ContinuationToken"] = continuation_token
    response = s3.list_objects_v2(**params)
    return normalize_s3_list(bucket_name, prefix, response)
