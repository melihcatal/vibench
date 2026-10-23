from __future__ import annotations

from typing import List, Optional

from storage_client import get_default_bucket, get_s3_client
from storage_models import ListedObject, normalize_s3_list


def list_objects_with_prefix(bucket: str, prefix: str = "", region: Optional[str] = None) -> List[ListedObject]:
    resolved_bucket = get_default_bucket(bucket)
    s3 = get_s3_client(region=region)
    paginator = s3.get_paginator("list_objects_v2")

    items: List[ListedObject] = []
    for page in paginator.paginate(Bucket=resolved_bucket, Prefix=prefix):
        items.extend(normalize_s3_list(page.get("Contents")))
    return items
