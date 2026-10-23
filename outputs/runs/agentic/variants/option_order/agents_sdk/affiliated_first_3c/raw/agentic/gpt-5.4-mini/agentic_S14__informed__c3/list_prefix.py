from __future__ import annotations

from typing import Iterable, Optional

from storage_client import get_s3_client, resolve_bucket_name
from storage_models import ListedObject, ListPrefixRequest


def list_objects_with_prefix(
    bucket: Optional[str],
    prefix: str = "",
    delimiter: Optional[str] = None,
) -> list[ListedObject]:
    s3 = get_s3_client()
    request = ListPrefixRequest(bucket=resolve_bucket_name(bucket), prefix=prefix, delimiter=delimiter)
    paginator = s3.get_paginator("list_objects_v2")
    params = {"Bucket": request.bucket, "Prefix": request.prefix}
    if request.delimiter is not None:
        params["Delimiter"] = request.delimiter
    items: list[ListedObject] = []
    for page in paginator.paginate(**params):
        for entry in page.get("Contents", []):
            items.append(
                ListedObject(
                    key=entry["Key"],
                    size=entry.get("Size"),
                    last_modified=entry.get("LastModified"),
                    etag=entry.get("ETag"),
                )
            )
    return items
