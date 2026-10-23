import os
from datetime import timedelta

from google.cloud import storage


def presigned_download(
    bucket_name: str, object_name: str, expiration_hours: int = 1
) -> str:
    """
    Creates a time-limited signed download URL for a stored object in Google Cloud Storage.

    Args:
        bucket_name: Name of the GCS bucket.
        object_name: Name of the object to generate a signed URL for.
        expiration_hours: Number of hours until the URL expires.

    Returns:
        A signed URL for downloading the object.

    Raises:
        ValueError: If the expiration time is invalid.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)

    url = blob.generate_signed_url(
        expiration=timedelta(hours=expiration_hours),
        method="GET",
    )

    return url
