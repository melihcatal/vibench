import os
from google.cloud import storage
from datetime import datetime, timedelta

def create_presigned_download_url(bucket_name, blob_name, expiration_hours=1):
    """Create a time-limited signed download URL for a GCS object.

    bucket_name: str - GCS bucket name
    blob_name: str - object name in bucket
    expiration_hours: int - hours until URL expires (default 1 hour)
    Returns:
        str - presigned URL
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    # Generate signed URL valid for the given duration
    url = blob.generate_signed_url(version="v4", expiration=timedelta(hours=expiration_hours), method="GET")
    print(f"Signed download URL for gs://{bucket_name}/{blob_name}: {url}")
    return url
