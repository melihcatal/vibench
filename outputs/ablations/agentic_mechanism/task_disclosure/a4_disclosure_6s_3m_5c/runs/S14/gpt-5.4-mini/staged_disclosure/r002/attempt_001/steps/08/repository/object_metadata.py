import os
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError


def read_object_metadata(bucket: str, key: str, region_name: Optional[str] = None) -> Dict[str, Any]:
    s3 = boto3.client("s3", region_name=region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))
    try:
        response = s3.head_object(Bucket=bucket, Key=key)
    except (BotoCoreError, ClientError) as exc:
        raise RuntimeError(f"Unable to read metadata for s3://{bucket}/{key}") from exc

    metadata = dict(response)
    if "ResponseMetadata" in metadata:
        metadata["ResponseMetadata"] = dict(metadata["ResponseMetadata"])
    return metadata


def read_object_head(bucket: str, key: str, region_name: Optional[str] = None) -> Dict[str, Any]:
    metadata = read_object_metadata(bucket, key, region_name=region_name)
    return {
        "etag": metadata.get("ETag"),
        "content_length": metadata.get("ContentLength"),
        "content_type": metadata.get("ContentType"),
        "last_modified": metadata.get("LastModified"),
        "metadata": metadata.get("Metadata", {}),
        "storage_class": metadata.get("StorageClass"),
    }
