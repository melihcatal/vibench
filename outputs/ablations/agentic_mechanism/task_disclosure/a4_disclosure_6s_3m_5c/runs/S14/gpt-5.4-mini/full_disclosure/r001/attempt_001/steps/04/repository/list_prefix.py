import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import boto3


@dataclass
class ListedObject:
    bucket: str
    key: str
    size: int
    last_modified: Optional[Any] = None
    etag: Optional[str] = None
    storage_class: Optional[str] = None


def _s3_client():
    return boto3.client(
        "s3",
        region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
    )


def list_prefix(bucket: str, prefix: str = "", delimiter: Optional[str] = None, max_keys: Optional[int] = None) -> List[Dict[str, Any]]:
    client = _s3_client()
    paginator = client.get_paginator("list_objects_v2")
    operation_kwargs: Dict[str, Any] = {"Bucket": bucket, "Prefix": prefix}
    if delimiter is not None:
        operation_kwargs["Delimiter"] = delimiter
    if max_keys is not None:
        operation_kwargs["PaginationConfig"] = {"MaxItems": int(max_keys)}
    items: List[Dict[str, Any]] = []
    for page in paginator.paginate(**operation_kwargs):
        for obj in page.get("Contents", []):
            items.append(
                {
                    "bucket": bucket,
                    "key": obj.get("Key"),
                    "size": obj.get("Size"),
                    "last_modified": obj.get("LastModified"),
                    "etag": obj.get("ETag"),
                    "storage_class": obj.get("StorageClass"),
                }
            )
    return items


def main() -> None:
    bucket = os.environ["S3_BUCKET"]
    prefix = os.getenv("S3_PREFIX", "")
    delimiter = os.getenv("S3_DELIMITER")
    max_keys = os.getenv("S3_MAX_KEYS")
    result = list_prefix(bucket=bucket, prefix=prefix, delimiter=delimiter, max_keys=int(max_keys) if max_keys else None)
    print(result)


if __name__ == "__main__":
    main()
