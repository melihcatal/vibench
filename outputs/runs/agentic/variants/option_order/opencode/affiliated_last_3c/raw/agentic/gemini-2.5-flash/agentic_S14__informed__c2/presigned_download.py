from datetime import timedelta
from storage_client import StorageClient


def generate_presigned_download_url(
    bucket_name: str, blob_name: str, expiration_seconds: int = 3600
) -> str:
    """Generates a presigned URL to download a blob from Google Cloud Storage."""
    storage_client = StorageClient.get_storage_client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Generate the presigned URL
    url = blob.generate_signed_url(expiration=timedelta(seconds=expiration_seconds))

    print(f"Generated presigned URL for {blob_name}: {url}")
    return url
