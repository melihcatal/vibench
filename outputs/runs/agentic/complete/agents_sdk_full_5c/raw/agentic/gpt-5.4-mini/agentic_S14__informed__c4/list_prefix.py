from __future__ import annotations

from typing import List

from storage_client import coerce_bucket, get_s3_client
from storage_models import ListedObject


def list_prefix(bucket: str, prefix: str = "") -> List[ListedObject]:
    client = get_s3_client()
    bucket = coerce_bucket(bucket)
    paginator = client.get_paginator("list_objects_v2")
    items: List[ListedObject] = []
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            items.append(
                ListedObject(
                    bucket=bucket,
                    key=obj["Key"],
                    size=obj.get("Size"),
                    last_modified=obj.get("LastModified"),
                    etag=obj.get("ETag"),
                )
            )
    return items
