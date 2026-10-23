import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError


@dataclass
class ObjectMetadataResult:
    bucket: str
    key: str
    exists: bool
    content_length: Optional[int] = None
    content_type: Optional[str] = None
    etag: Optional[str] = None
    last_modified: Optional[Any] = None
    storage_class: Optional[str] = None
    version_id: Optional[str] = None
    checksum: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, str]] = None
    raw: Optional[Dict[str, Any]] = None


def _s3_client(region_name: Optional[str] = None):
    return boto3.client("s3", region_name=region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))


def read_object_metadata(
    bucket: str,
    key: str,
    region_name: Optional[str] = None,
    version_id: Optional[str] = None,
) -> ObjectMetadataResult:
    client = _s3_client(region_name)
    params: Dict[str, Any] = {"Bucket": bucket, "Key": key}
    if version_id:
        params["VersionId"] = version_id
    try:
        response = client.head_object(**params)
    except ClientError as exc:
        error_code = exc.response.get("Error", {}).get("Code")
        if error_code in {"404", "NoSuchKey", "NotFound"}:
            return ObjectMetadataResult(bucket=bucket, key=key, exists=False)
        raise RuntimeError(f"failed to read object metadata for s3://{bucket}/{key}: {exc}") from exc
    except BotoCoreError as exc:
        raise RuntimeError(f"failed to read object metadata for s3://{bucket}/{key}: {exc}") from exc

    return ObjectMetadataResult(
        bucket=bucket,
        key=key,
        exists=True,
        content_length=response.get("ContentLength"),
        content_type=response.get("ContentType"),
        etag=response.get("ETag"),
        last_modified=response.get("LastModified"),
        storage_class=response.get("StorageClass"),
        version_id=response.get("VersionId"),
        checksum={
            k: response.get(k)
            for k in ("ChecksumCRC32", "ChecksumCRC32C", "ChecksumCRC64NVME", "ChecksumSHA1", "ChecksumSHA256")
            if response.get(k) is not None
        }
        or None,
        metadata=response.get("Metadata") or None,
        raw=response,
    )


def object_exists(bucket: str, key: str, region_name: Optional[str] = None, version_id: Optional[str] = None) -> bool:
    return read_object_metadata(bucket=bucket, key=key, region_name=region_name, version_id=version_id).exists
