import os
from pathlib import Path
from typing import BinaryIO, Optional, Union

import boto3

from storage_client import create_s3_client, get_storage_config
from storage_models import UploadResult, read_bytes_source


def upload_object(bucket: str, key: str, source: Union[str, bytes, bytearray, BinaryIO], content_type: Optional[str] = None, metadata: Optional[dict] = None) -> UploadResult:
    config = get_storage_config()
    client = create_s3_client(config)
    body = read_bytes_source(source)
    extra_args = {}
    if content_type:
        extra_args["ContentType"] = content_type
    if metadata:
        extra_args["Metadata"] = metadata
    client.put_object(Bucket=bucket, Key=key, Body=body, **extra_args)
    return UploadResult(bucket=bucket, key=key, size=len(body), etag=None)
