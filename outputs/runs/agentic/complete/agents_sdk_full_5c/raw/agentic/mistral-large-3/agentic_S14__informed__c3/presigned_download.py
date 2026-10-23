import os
from datetime import timedelta
from storage_client import get_storage_client

def generate_presigned_download_url(bucket_name: str, object_key: str, expiration_hours: int = 1) -> str:
    """
    Creates a time-limited signed download URL for a Google Cloud Storage object.
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable.
    """
    client = get_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_key)

    url = blob.generate_signed_url(
        expiration=timedelta(hours=expiration_hours),
        method="GET"
    )
    return url