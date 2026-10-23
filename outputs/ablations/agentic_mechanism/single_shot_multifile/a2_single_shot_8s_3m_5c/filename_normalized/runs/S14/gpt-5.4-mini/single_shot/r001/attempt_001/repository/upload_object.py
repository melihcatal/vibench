import os
from pathlib import Path
from typing import Any, BinaryIO, Optional, Union

import boto3

from storage_client import get_s3_client, get_storage_config
from storage_models import UploadRequest, UploadResponse, coerce_body_bytes


 def upload_object(request: UploadRequest) -> UploadResponse:
    config = get_storage_config()
    client = get_s3_client(config)
    body = coerce_body_bytes(request.body)
    extra_args = {}
    if request.content_type:
        extra_args["ContentType"] = request.content_type
    if request.metadata:
        extra_args["Metadata"] = request.metadata
    client.put_object(Bucket=request.bucket, Key=request.key, Body=body, **extra_args)
    return UploadResponse(bucket=request.bucket, key=request.key, size=len(body), etag=None)
