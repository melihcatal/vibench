from __future__ import annotations

from typing import List

from storage_client import get_bucket
from storage_models import ObjectListItem, normalize_items


def list_objects_with_prefix(bucket_name: str, prefix: str) -> List[ObjectListItem]:
    bucket = get_bucket(bucket_name)
    iterator = bucket.list_blobs(prefix=prefix)
    return normalize_items(iterator)
