# Create a time-limited signed download URL for a stored object (AWS S3 provider)
import os
from datetime import datetime, timedelta
from storage_client import create_s3_client


def presigned_download_url(
    bucket: str, key: str, expires_in_seconds: int = 3600
) -> str:
    """Generate a presigned URL valid for `expires_in_seconds` seconds."""
    client = create_s3_client()
    expiry = datetime.utcnow() + timedelta(seconds=expires_in_seconds)
    url = client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expires_in_seconds,
    )
    return url
