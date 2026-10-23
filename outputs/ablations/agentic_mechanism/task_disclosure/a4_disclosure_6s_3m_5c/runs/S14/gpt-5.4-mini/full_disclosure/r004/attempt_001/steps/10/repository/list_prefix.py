import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Iterator, List, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError


@dataclass
class ObjectListItem:
    key: str
    size: int
    last_modified: Optional[Any] = None
    etag: Optional[str] = None
    storage_class: Optional[str] = None
    owner_id: Optional[str] = None
    owner_display_name: Optional[str] = None


@dataclass
class PrefixListResult:
    bucket: str
    prefix: str
    items: List[ObjectListItem]
    count: int
    truncated: bool
    next_continuation_token: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None


def _s3_client(region_name: Optional[str] = None):
    return boto3.client("s3", region_name=region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))


def _iter_objects(client, bucket: str, prefix: str, delimiter: Optional[str] = None) -> Iterator[Dict[str, Any]]:
    paginator = client.get_paginator("list_objects_v2")
    params: Dict[str, Any] = {"Bucket": bucket, "Prefix": prefix}
    if delimiter:
        params["Delimiter"] = delimiter
    for page in paginator.paginate(**params):
        for item in page.get("Contents", []) or []:
            yield item


def list_prefix(
    bucket: str,
    prefix: str = "",
    region_name: Optional[str] = None,
    delimiter: Optional[str] = None,
    max_items: Optional[int] = None,
) -> PrefixListResult:
    client = _s3_client(region_name)
    params: Dict[str, Any] = {"Bucket": bucket, "Prefix": prefix}
    if delimiter:
        params["Delimiter"] = delimiter
    if max_items is not None and max_items > 0:
        params["MaxKeys"] = max_items
    try:
        response = client.list_objects_v2(**params)
    except (BotoCoreError, ClientError) as exc:
        raise RuntimeError(f"failed to list objects under s3://{bucket}/{prefix}: {exc}") from exc

    items = [
        ObjectListItem(
            key=obj.get("Key", ""),
            size=int(obj.get("Size") or 0),
            last_modified=obj.get("LastModified"),
            etag=obj.get("ETag"),
            storage_class=obj.get("StorageClass"),
            owner_id=(obj.get("Owner") or {}).get("ID"),
            owner_display_name=(obj.get("Owner") or {}).get("DisplayName"),
        )
        for obj in response.get("Contents", []) or []
    ]
    return PrefixListResult(
        bucket=bucket,
        prefix=prefix,
        items=items,
        count=len(items),
        truncated=bool(response.get("IsTruncated")),
        next_continuation_token=response.get("NextContinuationToken"),
        raw=response,
    )


def list_prefix_keys(
    bucket: str,
    prefix: str = "",
    region_name: Optional[str] = None,
    delimiter: Optional[str] = None,
    max_items: Optional[int] = None,
) -> List[str]:
    return [item.key for item in list_prefix(bucket, prefix=prefix, region_name=region_name, delimiter=delimiter, max_items=max_items).items]
