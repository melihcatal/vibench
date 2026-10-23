import base64
import mimetypes
import os
from dataclasses import dataclass
from typing import Any, BinaryIO, Dict, Optional, Union

import boto3
from botocore.exceptions import BotoCoreError, ClientError


BytesLike = Union[bytes, bytearray, memoryview]
UploadSource = Union[str, os.PathLike, BytesLike, BinaryIO]


@dataclass
class ManagedObjectUploadResult:
    bucket: str
    key: str
    etag: Optional[str] = None
    version_id: Optional[str] = None
    url: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


def _s3_client(region_name: Optional[str] = None):
    return boto3.client("s3", region_name=region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))


def _read_source(source: UploadSource) -> tuple[bytes, Optional[str]]:
    if isinstance(source, (bytes, bytearray, memoryview)):
        return bytes(source), None
    if isinstance(source, (str, os.PathLike)):
        path = os.fspath(source)
        with open(path, "rb") as f:
            return f.read(), path
    if hasattr(source, "read"):
        data = source.read()
        if isinstance(data, str):
            data = data.encode("utf-8")
        return bytes(data), getattr(source, "name", None)
    raise TypeError("source must be bytes, path-like, or a binary file object")


def upload_object(
    bucket: str,
    key: str,
    source: UploadSource,
    content_type: Optional[str] = None,
    metadata: Optional[Dict[str, str]] = None,
    region_name: Optional[str] = None,
    extra_args: Optional[Dict[str, Any]] = None,
) -> ManagedObjectUploadResult:
    data, filename = _read_source(source)
    client = _s3_client(region_name)
    resolved_content_type = content_type
    if not resolved_content_type and filename:
        resolved_content_type, _ = mimetypes.guess_type(filename)
    kwargs: Dict[str, Any] = {"Bucket": bucket, "Key": key, "Body": data}
    if resolved_content_type:
        kwargs["ContentType"] = resolved_content_type
    if metadata:
        kwargs["Metadata"] = metadata
    if extra_args:
        kwargs.update(extra_args)
    try:
        response = client.put_object(**kwargs)
    except (BotoCoreError, ClientError) as exc:
        raise RuntimeError(f"failed to upload object to s3://{bucket}/{key}: {exc}") from exc
    etag = response.get("ETag")
    version_id = response.get("VersionId")
    region = client.meta.region_name or region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    url = f"https://{bucket}.s3.{region}.amazonaws.com/{key}" if region else None
    return ManagedObjectUploadResult(bucket=bucket, key=key, etag=etag, version_id=version_id, url=url, metadata=metadata)


def upload_object_from_base64(
    bucket: str,
    key: str,
    data_base64: str,
    content_type: Optional[str] = None,
    metadata: Optional[Dict[str, str]] = None,
    region_name: Optional[str] = None,
) -> ManagedObjectUploadResult:
    return upload_object(bucket, key, base64.b64decode(data_base64), content_type=content_type, metadata=metadata, region_name=region_name)
