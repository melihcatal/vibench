import os
from typing import Any, Dict, List, Optional

import boto3


def _client():
    return boto3.client(
        "s3",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.environ.get("AWS_SESSION_TOKEN"),
        region_name=os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION"),
        endpoint_url=os.environ.get("AWS_S3_ENDPOINT_URL"),
    )


def list_prefix(bucket: str, prefix: str = "", delimiter: Optional[str] = None, max_keys: Optional[int] = None) -> Dict[str, Any]:
    client = _client()
    kwargs: Dict[str, Any] = {"Bucket": bucket, "Prefix": prefix}
    if delimiter is not None:
        kwargs["Delimiter"] = delimiter
    if max_keys is not None:
        kwargs["MaxKeys"] = int(max_keys)
    paginator = client.get_paginator("list_objects_v2")
    objects: List[Dict[str, Any]] = []
    common_prefixes: List[str] = []
    for page in paginator.paginate(**kwargs):
        for item in page.get("Contents", []):
            objects.append(
                {
                    "key": item.get("Key"),
                    "last_modified": item.get("LastModified").isoformat() if item.get("LastModified") else None,
                    "etag": item.get("ETag"),
                    "size": item.get("Size"),
                    "storage_class": item.get("StorageClass"),
                }
            )
        for item in page.get("CommonPrefixes", []):
            prefix_value = item.get("Prefix")
            if prefix_value is not None:
                common_prefixes.append(prefix_value)
        if max_keys is not None and len(objects) >= max_keys:
            objects = objects[: int(max_keys)]
            break
    return {"bucket": bucket, "prefix": prefix, "delimiter": delimiter, "objects": objects, "common_prefixes": common_prefixes}


def _load_args() -> tuple[str, str, Optional[str], Optional[int]]:
    bucket = os.environ["OBJECT_STORAGE_BUCKET"]
    prefix = os.environ.get("OBJECT_STORAGE_PREFIX", "")
    delimiter = os.environ.get("OBJECT_STORAGE_DELIMITER")
    max_keys_env = os.environ.get("OBJECT_STORAGE_MAX_KEYS")
    max_keys = int(max_keys_env) if max_keys_env else None
    return bucket, prefix, delimiter, max_keys


def main() -> None:
    bucket, prefix, delimiter, max_keys = _load_args()
    result = list_prefix(bucket, prefix=prefix, delimiter=delimiter, max_keys=max_keys)
    print(result)


if __name__ == "__main__":
    main()
