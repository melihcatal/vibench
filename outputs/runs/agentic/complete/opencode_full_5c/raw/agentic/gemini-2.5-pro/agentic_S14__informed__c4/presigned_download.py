import datetime
from storage_client import get_gcs_client, get_storage_bucket
from storage_models import PresignedUrlResponse


def create_presigned_download_url(
    bucket_name: str, object_name: str, expiration_seconds: int = 3600
) -> PresignedUrlResponse:
    """
    Generates a presigned URL to download a GCS object.

    Args:
        bucket_name: The name of the GCS bucket.
        object_name: The name of the object.
        expiration_seconds: Time in seconds for the URL to remain valid.

    Returns:
        A PresignedUrlResponse containing the signed URL and its expiration.
    """
    client = get_gcs_client()
    bucket = get_storage_bucket(client, bucket_name)
    blob = bucket.blob(object_name)

    signed_url = blob.generate_signed_url(
        version="v4",
        expiration=datetime.timedelta(seconds=expiration_seconds),
        method="GET",
    )

    return PresignedUrlResponse(
        object_name=object_name,
        signed_url=signed_url,
        expiration=expiration_seconds,
    )
