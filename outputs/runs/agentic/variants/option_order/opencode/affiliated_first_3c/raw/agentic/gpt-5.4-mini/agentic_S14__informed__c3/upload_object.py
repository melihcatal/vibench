import os
from typing import Any, Union

import boto3
from botocore.client import Config

from storage_client import get_s3_client
from storage_models import UploadRequest, UploadResponse, normalize_body, normalize_metadata, normalize_object_location


def upload_object(bucket: str, key: str, body: Union[str, bytes, bytearray, Any], content_type: str | None = None, metadata: dict | None = None, acl: str | None = None, s3_client=None) -> UploadResponse:
    client = s3_client or get_s3_client()
    request = UploadRequest(bucket=bucket, key=key, body=body, content_type=content_type, metadata=metadata, acl=acl)
    extra_args = {}
    if request.content_type:
        extra_args["ContentType"] = request.content_type
    if request.metadata:
        extra_args["Metadata"] = normalize_metadata(request.metadata)
    if request.acl:
        extra_args["ACL"] = request.acl
    body_value = normalize_body(request.body)
    if extra_args:
        client.put_object(Bucket=request.bucket, Key=request.key, Body=body_value, **extra_args)
    else:
        client.put_object(Bucket=request.bucket, Key=request.key, Body=body_value)
    return UploadResponse(**normalize_object_location(request.bucket, request.key))
