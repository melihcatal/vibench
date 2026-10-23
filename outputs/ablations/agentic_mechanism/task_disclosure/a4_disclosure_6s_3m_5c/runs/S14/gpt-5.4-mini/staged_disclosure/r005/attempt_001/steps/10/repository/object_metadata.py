import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError


@dataclass
class ObjectMetadata:
    bucket: str
    key: str
    content_length: Optional[int]
    content_type: Optional[str]
    etag: Optional[str]
    last_modified: Optional[str]
    metadata: Dict[str, str]
    storage_class: Optional[str]


def read_object_metadata(bucket: str, key: str, region_name: Optional[str] = None) -> ObjectMetadata:
    session = boto3.session.Session(region_name=region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))
    client = session.client("s3")
    try:
        response = client.head_object(Bucket=bucket, Key=key)
    except (ClientError, BotoCoreError) as exc:
        raise RuntimeError(f"Failed to read S3 object metadata for s3://{bucket}/{key}") from exc

    return ObjectMetadata(
        bucket=bucket,
        key=key,
        content_length=response.get("ContentLength"),
        content_type=response.get("ContentType"),
        etag=response.get("ETag"),
        last_modified=response.get("LastModified").isoformat() if response.get("LastModified") else None,
        metadata=response.get("Metadata", {}),
        storage_class=response.get("StorageClass"),
    )


def read_object_head(bucket: str, key: str, region_name: Optional[str] = None) -> Dict[str, Any]:
    session = boto3.session.Session(region_name=region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))
    client = session.client("s3")
    try:
        return client.head_object(Bucket=bucket, Key=key)
    except (ClientError, BotoCoreError) as exc:
        raise RuntimeError(f"Failed to read S3 object head for s3://{bucket}/{key}") from exc
