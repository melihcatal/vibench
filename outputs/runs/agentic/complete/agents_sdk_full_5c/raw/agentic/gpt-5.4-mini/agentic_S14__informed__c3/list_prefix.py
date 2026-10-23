from __future__ import annotations

from typing import Any

from storage_client import create_storage_client
from storage_models import ObjectListing, PrefixListRequest


def list_objects_under_prefix(request: PrefixListRequest) -> ObjectListing:
    s3 = create_storage_client("s3")
    kwargs: dict[str, Any] = {"Bucket": request.bucket, "Prefix": request.prefix}
    if request.max_items is not None:
        kwargs["MaxKeys"] = request.max_items
    if request.continuation_token:
        kwargs["ContinuationToken"] = request.continuation_token
    response = s3.list_objects_v2(**kwargs)
    objects = response.get("Contents", []) or []
    common_prefixes = [p.get("Prefix", "") for p in response.get("CommonPrefixes", []) or []]
    return ObjectListing(
        bucket=request.bucket,
        prefix=request.prefix,
        objects=objects,
        common_prefixes=common_prefixes,
        next_token=response.get("NextContinuationToken"),
        raw=response,
    )
