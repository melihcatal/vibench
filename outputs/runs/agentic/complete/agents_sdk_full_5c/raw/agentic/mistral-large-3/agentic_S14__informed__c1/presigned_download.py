from storage_client import get_storage_client, get_bucket_name
from storage_models import PresignedDownloadResponse


def create_presigned_download_url(key: str, expires_in: int = 3600) -> PresignedDownloadResponse:
    """
    Create a time-limited signed download URL for an object in Amazon S3.
    """
    client = get_storage_client()
    bucket = get_bucket_name()

    url = client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expires_in,
    )

    return {
        "url": url,
        "expires_in": expires_in,
    }