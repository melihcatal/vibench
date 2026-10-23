import os

boto3 = __import__("boto3")
from storage_client import ManagedObjectStorageClient


def get_object_metadata(bucket: str, key: str) -> dict:
    """Retrieve metadata (HEAD) for an object stored in S3.

    Parameters:
        bucket (str): Bucket name.
        key (str): Object key/path.

    Returns:
        dict: Metadata returned by S3 HEAD request.
    """
    s3 = ManagedObjectStorageClient(
        service="Amazon S3",
        credentials={
            "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID"),
            "AWS_SECRET_ACCESS_KEY": os.getenv("AWS_SECRET_ACCESS_KEY"),
        },
    )
    client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    response = client.head_object(Bucket=bucket, Key=key)
    return response
