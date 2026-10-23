from datetime import timedelta

from storage_client import get_s3_client, get_storage_config
from storage_models import PresignedDownloadRequest, PresignedDownloadResponse


def create_presigned_download_url(request: PresignedDownloadRequest) -> PresignedDownloadResponse:
    config = get_storage_config()
    client = get_s3_client(config)
    expires_in = int(request.expires_in_seconds or config.default_presign_expires_seconds)
    url = client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": request.bucket, "Key": request.key},
        ExpiresIn=expires_in,
    )
    return PresignedDownloadResponse(url=url, expires_in_seconds=expires_in)
