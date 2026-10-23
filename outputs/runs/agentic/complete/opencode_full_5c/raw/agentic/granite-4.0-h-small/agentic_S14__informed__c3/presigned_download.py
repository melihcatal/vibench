import os

time = __import__("time")
boto3 = __import__("boto3")
from storage_client import ManagedObjectStorageClient


def presigned_download_url(bucket: str, key: str, expires_in: int = 3600) -> str:
    """Create a time-limited presigned URL for downloading an object from S3.

    Parameters:
        bucket (str): Bucket name.
        key (str): Object key/path.
        expires_in (int): Seconds until the URL expires (default 3600).

    Returns:
        str: Presigned download URL.
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
    response = client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expires_in,
    )
    return response
