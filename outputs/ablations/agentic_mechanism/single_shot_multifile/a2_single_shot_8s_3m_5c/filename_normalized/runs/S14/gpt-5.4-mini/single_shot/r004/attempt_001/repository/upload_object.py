import base64
import mimetypes
import os
from typing import Any, BinaryIO, Optional, Union

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from storage_client import get_s3_client, resolve_bucket_name, resolve_object_key
from storage_models import UploadObjectRequest, UploadObjectResponse, normalize_etag


DataSource = Union[bytes, bytearray, str, BinaryIO]


def _read_data(data: DataSource) -> bytes:
    if isinstance(data, (bytes, bytearray)):
        return bytes(data)
    if isinstance(data, str):
        if os.path.exists(data):
            with open(data, "rb") as f:
                return f.read()
        try:
            return base64.b64decode(data, validate=True)
        except Exception:
            return data.encode("utf-8")
    return data.read()


def upload_object(request: UploadObjectRequest) -> UploadObjectResponse:
    client = get_s3_client()
    bucket = resolve_bucket_name(request.bucket)
    key = resolve_object_key(request.key)
    body = _read_data(request.data)
    content_type = request.content_type or mimetypes.guess_type(key)[0] or "application/octet-stream"
    extra_args = {"ContentType": content_type}
    if request.metadata:
        extra_args["Metadata"] = request.metadata
    if request.server_side_encryption:
        extra_args["ServerSideEncryption"] = request.server_side_encryption
    try:
        result = client.put_object(Bucket=bucket, Key=key, Body=body, **extra_args)
        return UploadObjectResponse(bucket=bucket, key=key, etag=normalize_etag(result.get("ETag")), version_id=result.get("VersionId"))
    except (ClientError, BotoCoreError) as exc:
        raise RuntimeError(f"s3 upload failed for s3://{bucket}/{key}: {exc}") from exc


__all__ = ["upload_object"]
