import mimetypes
import os
from dataclasses import dataclass
from typing import Any, BinaryIO, Optional, Union

import boto3


@dataclass
class UploadResult:
    bucket: str
    key: str
    etag: Optional[str]
    version_id: Optional[str]
    url: Optional[str]


def _client() -> Any:
    region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    if region:
        return boto3.client("s3", region_name=region)
    return boto3.client("s3")


def upload_object(
    bucket: str,
    key: str,
    data: Union[str, bytes, bytearray, BinaryIO],
    content_type: Optional[str] = None,
    metadata: Optional[dict[str, str]] = None,
    extra_args: Optional[dict[str, Any]] = None,
) -> UploadResult:
    s3 = _client()
    upload_args: dict[str, Any] = dict(extra_args or {})
    if content_type:
        upload_args["ContentType"] = content_type
    elif isinstance(data, str):
        guessed, _ = mimetypes.guess_type(data)
        if guessed:
            upload_args["ContentType"] = guessed
    if metadata:
        upload_args["Metadata"] = metadata

    if isinstance(data, str):
        s3.upload_file(data, bucket, key, ExtraArgs=upload_args or None)
    elif isinstance(data, (bytes, bytearray)):
        s3.put_object(Bucket=bucket, Key=key, Body=data, **upload_args)
    else:
        s3.upload_fileobj(data, bucket, key, ExtraArgs=upload_args or None)

    response = s3.head_object(Bucket=bucket, Key=key)
    return UploadResult(
        bucket=bucket,
        key=key,
        etag=response.get("ETag"),
        version_id=response.get("VersionId"),
        url=f"s3://{bucket}/{key}",
    )
