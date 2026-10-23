import os
import boto3
from storage_client import ManagedObjectStorageClient


def upload_object(bucket: str, key: str, file_path: str) -> dict:
    """Upload a local file or byte stream to Amazon S3.

    Parameters:
        bucket (str): Bucket name.
        key (str): Object key/path.
        file_path (str): Path to local file or directory.

    Returns:
        dict: Upload result metadata.
    """
    s3 = ManagedObjectStorageClient(
        service="Amazon S3",
        credentials={
            "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID"),
            "AWS_SECRET_ACCESS_KEY": os.getenv("AWS_SECRET_ACCESS_KEY"),
        },
    )
    return s3.upload(bucket, key, file_path)
