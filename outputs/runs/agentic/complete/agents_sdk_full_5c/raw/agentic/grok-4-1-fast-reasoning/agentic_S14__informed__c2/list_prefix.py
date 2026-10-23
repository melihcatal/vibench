from storage_client import get_s3_client, get_bucket_name
from storage_models import ListObjectsResponse
from typing import Dict, Any, List

def list_prefix(
    prefix: str,
    bucket_name: str | None = None,
    delimiter: str = "/",
    max_keys: int = 1000
) -> ListObjectsResponse:
    if bucket_name is None:
        bucket_name = get_bucket_name()
    client = get_s3_client()
    kwargs = {
        "Bucket": bucket_name,
        "Prefix": prefix,
        "Delimiter": delimiter,
        "MaxKeys": max_keys
    }
    resp = client.list_objects_v2(**kwargs)
    objects = [
        {
            "key": obj["Key"],
            "size": obj["Size"],
            "last_modified": str(obj["LastModified"]),
            "etag": obj["ETag"].strip('"')
        }
        for obj in resp.get("Contents", [])
    ]
    prefixes = [pre["Prefix"] for pre in resp.get("CommonPrefixes", [])]
    return {
        "objects": objects,
        "prefixes": prefixes,
        "is_truncated": resp.get("IsTruncated", False),
        "next_continuation_token": resp.get("NextContinuationToken")
    }
