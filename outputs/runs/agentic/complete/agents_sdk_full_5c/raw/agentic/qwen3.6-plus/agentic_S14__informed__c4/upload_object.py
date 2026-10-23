"""
upload_object.py — Upload a file or byte stream to managed object storage.

Concrete provider: Amazon S3 via boto3 SDK.
Provider signals:
  - boto3 import
  - "s3" client creation
  - AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY environment variables
"""

import os
from typing import BinaryIO, Optional, Dict, Union
from botocore.exceptions import ClientError

from storage_client import S3StorageClient
from storage_models import UploadResult


def upload_object(
    bucket: str,
    key: str,
    data: Union[bytes, BinaryIO, str],
    content_type: Optional[str] = None,
    metadata: Optional[Dict[str, str]] = None,
    storage_class: Optional[str] = None,
) -> UploadResult:
    """
    Upload data (bytes, file-like object, or string) as an S3 object.

    Parameters
    ----------
    bucket : str
        Target S3 bucket name.
    key : str
        S3 object key (path within the bucket).
    data : bytes | BinaryIO | str
        Content to upload. Strings are UTF-8 encoded.
    content_type : str, optional
        MIME type for the uploaded object.
    metadata : dict, optional
        User metadata key-value pairs to attach.
    storage_class : str, optional
        S3 storage class (e.g., STANDARD, INTELLIGENT_TIERING, GLACIER).

    Returns
    -------
    UploadResult
        Normalized upload result with etag, version_id, etc.

    Raises
    ------
    ClientError
        When the underlying S3 PutObject call fails.
    """
    client = S3StorageClient(bucket=bucket).get_client()

    put_kwargs: Dict = {
        "Bucket": bucket,
        "Key": key,
        "Body": data,
    }

    if content_type:
        put_kwargs["ContentType"] = content_type
    if metadata:
        put_kwargs["Metadata"] = metadata
    if storage_class:
        put_kwargs["StorageClass"] = storage_class

    response = client.put_object(**put_kwargs)

    result = UploadResult.from_s3_response(bucket, key, response)
    result.content_length = response.get("ContentLength", 0)

    return result


def upload_from_file_path(
    bucket: str,
    key: str,
    file_path: str,
    content_type: Optional[str] = None,
    metadata: Optional[Dict[str, str]] = None,
    storage_class: Optional[str] = None,
) -> UploadResult:
    """
    Convenience: upload a local file to S3 using multipart when needed.

    Uses boto3's S3 Transfer Manager for large files.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Local file not found: {file_path}")

    client = S3StorageClient(bucket=bucket).get_client()

    extra_args: Dict = {}
    if content_type:
        extra_args["ContentType"] = content_type
    if metadata:
        extra_args["Metadata"] = metadata
    if storage_class:
        extra_args["StorageClass"] = storage_class

    client.upload_file(
        Filename=file_path,
        Bucket=bucket,
        Key=key,
        ExtraArgs=extra_args,
    )

    # Retrieve head to populate result fields
    head = client.head_object(Bucket=bucket, Key=key)
    return UploadResult.from_s3_response(bucket, key, head)
