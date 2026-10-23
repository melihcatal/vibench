from datetime import datetime, timedelta, timezone
from .storage_client import get_bucket

def generate_download_url(object_name: str, expiration_minutes: int = 60) -> str:
    """
    Generates a presigned URL to download an object from Google Cloud Storage.

    Args:
        object_name (str): The name of the object in the bucket.
        expiration_minutes (int): The number of minutes the URL should be valid for.

    Returns:
        str: The presigned URL for the object.
    """
    bucket = get_bucket()
    blob = bucket.blob(object_name)

    expiration_time = timedelta(minutes=expiration_minutes)

    # The google-cloud-storage library uses a datetime object for expiration.
    url = blob.generate_signed_url(
        version="v4",
        expiration=expiration_time,
        method="GET",
    )

    return url
