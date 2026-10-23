import os
from io import BytesIO
from typing import Union

import boto3

from storage_client import get_s3_client, get_bucket_name
from storage_models import UploadRequest, UploadResult, normalize_body, infer_content_type, object_key_from_input


def upload_object(source: Union[str, bytes, bytearray, BytesIO], bucket: str = None, key: str = None, content_type: str = None) -> UploadResult:
    request = UploadRequest.from_source(source, bucket=bucket, key=key, content_type=content_type)
    client = get_s3_client()
    client.put_object(Bucket=request.bucket, Key=request.key, Body=normalize_body(request.body), ContentType=request.content_type)
    return UploadResult(bucket=request.bucket, key=request.key, content_type=request.content_type)
