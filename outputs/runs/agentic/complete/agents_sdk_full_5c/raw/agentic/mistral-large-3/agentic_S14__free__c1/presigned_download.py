from google.cloud import storage
from storage_client import get_storage_client, get_bucket_name
from storage_models import PresignedDownloadResponse
from datetime import timedelta


def generate_presigned_download(object_name: str, expiration_hours: int = 1) -> PresignedDownloadResponse:
    """
    Generate a time-limited signed download URL for a Google Cloud Storage object.
    
    Args:
        object_name: Name of the object in the bucket.
        expiration_hours: Number of hours until the URL expires.
        
    Returns:
        PresignedDownloadResponse containing the signed URL and expiration time.
    """
    client = get_storage_client()
    bucket_name = get_bucket_name()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    
    url = blob.generate_signed_url(
        expiration=timedelta(hours=expiration_hours),
        method="GET"
    )
    
    return PresignedDownloadResponse(
        url=url,
        expires_in_seconds=expiration_hours * 3600
    )