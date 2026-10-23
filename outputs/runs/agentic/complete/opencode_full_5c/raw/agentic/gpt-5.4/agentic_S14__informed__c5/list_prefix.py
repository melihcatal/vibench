from __future__ import annotations

from storage_client import get_s3_client
from storage_models import ListPrefixResult, normalize_listed_object


def list_prefix(
    bucket: str,
    prefix: str,
    continuation_token: str | None = None,
    max_keys: int = 1000,
) -> ListPrefixResult:
    s3 = get_s3_client()
    params: dict[str, object] = {
        "Bucket": bucket,
        "Prefix": prefix,
        "MaxKeys": max_keys,
    }
    if continuation_token:
        params["ContinuationToken"] = continuation_token
    response = s3.list_objects_v2(**params)
    objects = [normalize_listed_object(item) for item in response.get("Contents", [])]
    return ListPrefixResult(
        bucket=bucket,
        prefix=prefix,
        objects=objects,
        next_token=response.get("NextContinuationToken"),
    )
