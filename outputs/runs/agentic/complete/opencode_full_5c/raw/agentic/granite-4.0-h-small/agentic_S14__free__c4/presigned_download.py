import boto3
from storage_client import get_managed_storage_client


def presigned_download_url(
    bucket_name: str, object_key: str, expires_seconds: int = 3600
) -> str:
    """Create a time-limited presigned download URL for an object.

    Uses AWS S3-compatible managed object storage.
    """
    client = get_managed_storage_client()
    response = client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket_name, "Key": object_key},
        ExpiresIn=expires_seconds,
    )
    return response
