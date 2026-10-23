from __future__ import annotations

from storage_client import get_s3_client
from storage_models import ListPrefixResponse, normalize_s3_list


def list_prefix(
    bucket: str,
    prefix: str,
    continuation_token: str | None = None,
    max_keys: int = 1000,
) -> ListPrefixResponse:
    s3 = get_s3_client()
    params: dict[str, object] = {
        "Bucket": bucket,
        "Prefix": prefix,
        "MaxKeys": max_keys,
    }
    if continuation_token:
        params["ContinuationToken"] = continuation_token
    payload = s3.list_objects_v2(**params)
    return normalize_s3_list(bucket, prefix, payload)
