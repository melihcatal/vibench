import datetime
from storage_client import get_storage_client


def generate_presigned_download_url(
    bucket_name: str, blob_name: str, expiration_minutes: int = 60
):
    """Generates a v4 signed URL for downloading a blob."""
    storage_client = get_storage_client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(
        version="v4",
        # This URL is valid for expiration_minutes minutes
        expiration=datetime.timedelta(minutes=expiration_minutes),
        # Allow GET requests using this URL.
        method="GET",
    )

    print(f"Generated GET signed URL for {blob.name} in bucket {bucket.name}.")
    print(f"The URL is valid for {expiration_minutes} minutes.")
    print("URL:", url)
    return url
