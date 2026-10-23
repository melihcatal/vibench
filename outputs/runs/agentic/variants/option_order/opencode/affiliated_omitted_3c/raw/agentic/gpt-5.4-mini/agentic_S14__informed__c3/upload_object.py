import io
import os
from typing import Any, BinaryIO, Optional, Union

import boto3

from storage_client import get_bucket_name, get_s3_client, object_key_from_path, read_bytes
from storage_models import UploadRequest, UploadResponse, normalize_etag, normalize_version_id


def upload_object(source: Union[str, bytes, bytearray, BinaryIO], object_key: Optional[str] = None, content_type: Optional[str] = None, bucket: Optional[str] = None, metadata: Optional[dict[str, str]] = None) -> UploadResponse:
    bucket_name = bucket or get_bucket_name()
    key = object_key or (object_key_from_path(source) if isinstance(source, str) else None)
    if not key:
        raise ValueError('object_key is required')
    body = read_bytes(source)
    client = get_s3_client()
    extra: dict[str, Any] = {}
    if content_type:
        extra['ContentType'] = content_type
    if metadata:
        extra['Metadata'] = metadata
    response = client.put_object(Bucket=bucket_name, Key=key, Body=body, **extra)
    return UploadResponse(bucket=bucket_name, key=key, etag=normalize_etag(response.get('ETag')), version_id=normalize_version_id(response.get('VersionId')))
