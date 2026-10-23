import os
from dataclasses import dataclass
from typing import BinaryIO, Optional, Union

import boto3


@dataclass
class UploadResult:
    bucket: str
    key: str
    version_id: Optional[str] = None
    etag: Optional[str] = None


def _s3_client():
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    return boto3.client("s3", region_name=region)


def upload_object(
    bucket: str,
    key: str,
    data: Union[str, bytes, BinaryIO],
    content_type: Optional[str] = None,
    metadata: Optional[dict] = None,
) -> UploadResult:
    client = _s3_client()
    extra_args = {}
    if content_type:
        extra_args["ContentType"] = content_type
    if metadata:
        extra_args["Metadata"] = metadata
    if isinstance(data, str):
        client.upload_file(data, bucket, key, ExtraArgs=extra_args or None)
    elif isinstance(data, bytes):
        client.put_object(Bucket=bucket, Key=key, Body=data, **extra_args)
    else:
        client.upload_fileobj(data, bucket, key, ExtraArgs=extra_args or None)
    head = client.head_object(Bucket=bucket, Key=key)
    return UploadResult(
        bucket=bucket,
        key=key,
        version_id=head.get("VersionId"),
        etag=head.get("ETag"),
    )
