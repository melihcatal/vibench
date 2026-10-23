import boto3
from storage_client import get_managed_storage_client


def upload_object(
    bucket_name: str, object_key: str, data: bytes, metadata: dict = None
) -> dict:
    """Upload a file or byte stream to managed object storage.

    Uses AWS S3-compatible managed object storage (e.g., Amazon S3, AWS Outposts, or compatible provider).
    """
    client = get_managed_storage_client()
    # If data is a file path, read bytes; otherwise assume already bytes
    if isinstance(data, str):
        with open(data, "rb") as f:
            data = f.read()
    response = client.put_object(
        Bucket=bucket_name, Key=object_key, Body=data, Metadata=metadata or {}
    )
    return response
