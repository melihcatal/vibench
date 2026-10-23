import boto3
from storage_client import get_s3_client

def get_object_metadata(bucket_name: str, object_key: str):
    """Retrieve metadata (head) of an object in managed object storage.

    Uses AWS S3 as the provider.
    """
    client = get_s3_client()
    response = client.head_object(Bucket=bucket_name, Key=object_key)
    return response  # contains metadata like ContentLength, ContentType, etc.