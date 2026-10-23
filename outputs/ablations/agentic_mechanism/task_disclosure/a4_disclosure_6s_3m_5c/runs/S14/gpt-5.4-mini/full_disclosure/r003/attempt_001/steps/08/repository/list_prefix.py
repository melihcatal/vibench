import os
from typing import Any, Dict, List, Optional

import boto3


def _client():
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
    return boto3.client("s3", region_name=region)


def list_prefix(bucket: str, prefix: str = "", delimiter: Optional[str] = None, max_keys: Optional[int] = None) -> Dict[str, Any]:
    kwargs: Dict[str, Any] = {"Bucket": bucket, "Prefix": prefix}
    if delimiter is not None:
        kwargs["Delimiter"] = delimiter
    if max_keys is not None:
        kwargs["MaxKeys"] = max_keys
    response = _client().list_objects_v2(**kwargs)
    objects: List[Dict[str, Any]] = []
    for item in response.get("Contents", []):
        objects.append(
            {
                "key": item.get("Key"),
                "last_modified": item.get("LastModified").isoformat() if item.get("LastModified") else None,
                "etag": item.get("ETag"),
                "size": item.get("Size"),
                "storage_class": item.get("StorageClass"),
            }
        )
    return {
        "bucket": bucket,
        "prefix": prefix,
        "delimiter": delimiter,
        "is_truncated": response.get("IsTruncated", False),
        "next_continuation_token": response.get("NextContinuationToken"),
        "objects": objects,
        "common_prefixes": [p.get("Prefix") for p in response.get("CommonPrefixes", [])],
    }


def main() -> None:
    bucket = os.environ["BUCKET"]
    prefix = os.getenv("PREFIX", "")
    delimiter = os.getenv("DELIMITER")
    max_keys = os.getenv("MAX_KEYS")
    result = list_prefix(bucket=bucket, prefix=prefix, delimiter=delimiter, max_keys=int(max_keys) if max_keys else None)
    print(result)


if __name__ == "__main__":
    main()
