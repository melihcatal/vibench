from datetime import datetime, timedelta, timezone
from . import storage_client

def generate_presigned_url(object_name: str) -> str:
    """Generates a presigned URL to download a file from GCS."""
    
    gcs_client = storage_client.get_storage_client()
    bucket_name = storage_client.get_default_bucket_name()
    if not bucket_name:
        raise ValueError("GCS_BUCKET_NAME environment variable not set.")

    bucket = gcs_client.bucket(bucket_name)
    blob = bucket.blob(object_name)

    # URL will be valid for 1 hour
    expiration_time = datetime.now(timezone.utc) + timedelta(hours=1)

    url = blob.generate_signed_url(
        version="v4",
        expiration=expiration_time,
        method="GET",
    )
    
    print(f"Generated presigned URL for {object_name}: {url}")
    return url
