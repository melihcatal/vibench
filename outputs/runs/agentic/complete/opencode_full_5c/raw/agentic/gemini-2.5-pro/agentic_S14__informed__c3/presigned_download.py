import datetime
from storage_client import get_storage_client
from storage_models import StorageObject, PresignedUrl


def create_presigned_download_url(
    storage_object: StorageObject, expiration_seconds: int = 3600
) -> PresignedUrl:
    """
    Generates a presigned URL to download a file from a GCS bucket.

    Args:
        storage_object: A StorageObject with bucket and key specified.
        expiration_seconds: Time in seconds for the presigned URL to remain valid.

    Returns:
        A PresignedUrl dataclass instance.
    """
    client = get_storage_client()
    bucket = client.bucket(storage_object.bucket)
    blob = bucket.blob(storage_object.key)

    url = blob.generate_signed_url(
        version="v4",
        expiration=datetime.timedelta(seconds=expiration_seconds),
        method="GET",
    )
    return PresignedUrl(url=url)
