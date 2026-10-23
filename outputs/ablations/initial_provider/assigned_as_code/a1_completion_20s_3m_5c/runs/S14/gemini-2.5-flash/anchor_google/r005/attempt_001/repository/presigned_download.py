from datetime import timedelta

from storage_client import get_storage_client
from storage_models import PresignedURLResponse

def create_presigned_download_url(payload, config=None):
    config = config or {}
    client = get_storage_client()
    bucket_name = config.get("bucket")
    if not bucket_name:
        raise ValueError("Bucket name not provided in config.")

    bucket = client.bucket(bucket_name)
    blob = bucket.blob(payload["object_name"])

    # Generate a v4 signed URL for downloading a blob.
    # The URL is valid for 1 hour by default.
    url = blob.generate_signed_url(
        version="v4",
        expiration=timedelta(minutes=60),  # This URL will be valid for 60 minutes
        method="GET",  # Allow GET requests using this URL.
    )
    return PresignedURLResponse(url=url).__dict__
