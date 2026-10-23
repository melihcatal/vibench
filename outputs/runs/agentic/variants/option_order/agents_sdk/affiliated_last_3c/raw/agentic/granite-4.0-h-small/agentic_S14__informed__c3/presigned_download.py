import os
from google.cloud import storage
from storage_client import get_storage_client

def presigned_download_url(bucket_name, blob_name, expiration_seconds=3600):
    """Create a time-limited signed URL for downloading an object from Google Cloud Storage.

    Args:
        bucket_name (str): Name of the bucket.
        blob_name (str): Name of the object (blob) in the bucket.
        expiration_seconds (int): Duration the URL is valid (default 1 hour).

    Returns:
        str: Signed URL to download the object.
    """
    client = get_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    url = blob.generate_signed_url(
        version="v4",
        expiration=datetime.timedelta(seconds=expiration_seconds),
        method="GET",
    )
    print(f'Presigned download URL for gs://{bucket_name}/{blob_name}: {url}')
    return url
