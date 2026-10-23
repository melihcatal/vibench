# upload_object.py
# [SAME-SCENARIO] upload object to Managed Object Storage
# Using AWS S3 as the concrete managed object storage provider
import json
import boto3
from typing import Union, BinaryIO

# Load configuration from local helper
from storage_client import get_s3_client


def upload_object(bucket: str, key: str, data: Union[str, bytes, BinaryIO]) -> dict:
    """Upload a file or byte stream to an S3 bucket.

    Returns the JSON response from S3.
    """
    s3 = get_s3_client()
    if isinstance(data, (str, bytes)):
        # For strings or bytes, upload as raw body
        body = data if isinstance(data, bytes) else data.encode("utf-8")
        response = s3.put_object(Bucket=bucket, Key=key, Body=body)
    else:
        # Assume a file-like object
        response = s3.upload_fileobj(Fileobj=data, Bucket=bucket, Key=key)
    return response
