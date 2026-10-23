from storage_client import get_s3_client
from storage_models import extract_keys
from typing import List


def list_objects_prefix(bucket: str, prefix: str = "") -> List[str]:
    client = get_s3_client()
    paginator = client.get_paginator("list_objects_v2")
    all_keys: List[str] = []
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        all_keys.extend(extract_keys(page.get("Contents", [])))
    return all_keys
