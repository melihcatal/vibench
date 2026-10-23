from __future__ import annotations

from typing import List, Optional

from storage_client import get_s3_client
from storage_models import ListedObject, normalize_listed_object


def list_objects(bucket: str, prefix: str = "", max_keys: Optional[int] = None) -> List[ListedObject]:
    s3 = get_s3_client()
    paginator = s3.get_paginator("list_objects_v2")
    pagination_config = {}
    if max_keys is not None:
        pagination_config["MaxItems"] = max_keys
    page_iterator = paginator.paginate(
        Bucket=bucket,
        Prefix=prefix,
        PaginationConfig=pagination_config or None,
    )
    results: List[ListedObject] = []
    for page in page_iterator:
        for item in page.get("Contents", []):
            results.append(normalize_listed_object(item))
            if max_keys is not None and len(results) >= max_keys:
                return results
    return results
