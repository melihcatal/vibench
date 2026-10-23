from typing import List
from storage_client import get_s3_client, get_bucket


def list_objects(prefix: str = "") -> List[str]:
    client = get_s3_client()
    bucket = get_bucket()
    paginator = client.get_paginator("list_objects_v2")
    keys = []
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            keys.append(obj["Key"])
    return keys
