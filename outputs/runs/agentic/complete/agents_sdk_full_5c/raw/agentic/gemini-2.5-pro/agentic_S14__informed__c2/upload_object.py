import os
from typing import IO

import boto3

from storage_client import get_s3_client


def upload_object(bucket_name: str, object_name: str, data: bytes | IO[bytes]):
    """
    Uploads a file or byte stream to an S3 bucket.

    :param bucket_name: The name of the S3 bucket.
    :param object_name: The name of the object in the bucket.
    :param data: The byte stream or file-like object to upload.
    """
    s3_client = get_s3_client()
    if isinstance(data, bytes):
        s3_client.put_object(Bucket=bucket_name, Key=object_name, Body=data)
    else:
        s3_client.upload_fileobj(data, bucket_name, object_name)
    print(f"Successfully uploaded '{object_name}' to bucket '{bucket_name}'.")

