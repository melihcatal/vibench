from storage_client import get_storage_client
from storage_models import ListedObject, normalize_list
from typing import List


def list_objects_prefix(bucket: str, prefix: str = "") -> List[ListedObject]:
    client = get_storage_client()
    paginator = client.get_paginator("list_objects_v2")
    all_objects: List[ListedObject] = []
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        contents = page.get("Contents", [])
        all_objects.extend(normalize_list(contents))
    return all_objects
