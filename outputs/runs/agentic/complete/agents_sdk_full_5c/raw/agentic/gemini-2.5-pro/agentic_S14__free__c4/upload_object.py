import os
from typing import Union, IO

from botocore.exceptions import ClientError
from storage_client import get_storage_client, get_bucket_name

def upload_file_to_storage(
    object_name: str, file_path: str, bucket_name: str = None
) -> bool:
    """
    Uploads a file from a local path to S3.

    :param object_name: The key (path) for the object in the bucket.
    :param file_path: The local path to the file to upload.
    :param bucket_name: The target S3 bucket. Defaults to env config.
    :return: True if upload was successful, else False.
    """
    s3_client = get_storage_client()
    target_bucket = bucket_name or get_bucket_name()
    try:
        s3_client.upload_file(file_path, target_bucket, object_name)
    except ClientError as e:
        print(f"Error uploading file: {e}")
        return False
    return True

def upload_bytes_to_storage(
    object_name: str, data: Union[bytes, IO[bytes]], bucket_name: str = None
) -> bool:
    """
    Uploads a byte stream or bytes object to S3.

    :param object_name: The key (path) for the object in the bucket.
    :param data: The bytes or file-like object to upload.
    :param bucket_name: The target S3 bucket. Defaults to env config.
    :return: True if upload was successful, else False.
    """
    s3_client = get_storage_client()
    target_bucket = bucket_name or get_bucket_name()
    try:
        s3_client.put_object(Bucket=target_bucket, Key=object_name, Body=data)
    except ClientError as e:
        print(f"Error uploading bytes: {e}")
        return False
    return True
