import os
from typing import Union

from storage_client import get_storage_client
from storage_models import UploadRequest


def upload_object(request: UploadRequest, content: Union[bytes, str]):
    """
    Uploads a file or byte stream to an S3 bucket.
    """
    s3_client = get_storage_client()

    if isinstance(content, str):
        body = content.encode("utf-8")
    else:
        body = content

    s3_client.put_object(
        Bucket=request.s3_object.bucket, Key=request.s3_object.key, Body=body
    )
    return {
        "status": "success",
        "bucket": request.s3_object.bucket,
        "key": request.s3_object.key,
    }


def upload_file(request: UploadRequest):
    """
    Uploads a local file to an S3 bucket.
    """
    s3_client = get_storage_client()
    s3_client.upload_file(
        request.source_file_path, request.s3_object.bucket, request.s3_object.key
    )
    return {
        "status": "success",
        "bucket": request.s3_object.bucket,
        "key": request.s3_object.key,
    }
