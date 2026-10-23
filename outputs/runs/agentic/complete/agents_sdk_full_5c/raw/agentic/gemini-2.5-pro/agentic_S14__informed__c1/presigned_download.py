import datetime
from google.cloud.storage import Bucket
from storage_client import get_storage_client, get_default_bucket_name

def generate_presigned_download_url(blob_name: str, expiration_seconds: int = 3600):
    """
    Generates a v4 presigned URL for downloading a blob.

    Args:
        blob_name (str): The name of the blob in the bucket.
        expiration_seconds (int): The number of seconds the URL is valid for.

    Returns:
        str: The presigned URL.
    """
    client = get_storage_client()
    bucket_name = get_default_bucket_name()
    bucket: Bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(
        version="v4",
        expiration=datetime.timedelta(seconds=expiration_seconds),
        method="GET",
    )
    return url
