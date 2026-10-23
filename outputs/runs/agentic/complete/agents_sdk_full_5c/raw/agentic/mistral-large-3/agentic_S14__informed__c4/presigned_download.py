from storage_client import StorageClient
from storage_models import PresignedDownloadResponse


def create_presigned_download(bucket: str, key: str, expires_in: int = 3600) -> PresignedDownloadResponse:
    """Creates a time-limited signed download URL for IBM Cloud Object Storage."""
    client = StorageClient().get_client()
    url = client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expires_in,
    )
    return PresignedDownloadResponse(url=url, expires_in=expires_in)