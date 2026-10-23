import os
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import ClientError


def _client():
    endpoint_url = os.environ.get("AWS_S3_ENDPOINT_URL")
    region_name = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    return boto3.client("s3", endpoint_url=endpoint_url, region_name=region_name)


def get_object_metadata(bucket: str, key: str) -> Dict[str, Any]:
    s3 = _client()
    response = s3.head_object(Bucket=bucket, Key=key)
    return {
        "bucket": bucket,
        "key": key,
        "content_length": response.get("ContentLength"),
        "content_type": response.get("ContentType"),
        "etag": response.get("ETag"),
        "last_modified": response.get("LastModified").isoformat() if response.get("LastModified") else None,
        "metadata": response.get("Metadata", {}),
        "storage_class": response.get("StorageClass"),
        "version_id": response.get("VersionId"),
    }


def head_object(bucket: str, key: str) -> Dict[str, Any]:
    return get_object_metadata(bucket, key)


def get_object_metadata_safe(bucket: str, key: str) -> Optional[Dict[str, Any]]:
    try:
        return get_object_metadata(bucket, key)
    except ClientError:
        return None
