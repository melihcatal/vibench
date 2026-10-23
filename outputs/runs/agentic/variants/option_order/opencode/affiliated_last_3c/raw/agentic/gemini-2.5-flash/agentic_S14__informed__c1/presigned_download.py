from storage_client import get_storage_client
from storage_models import PresignedDownloadRequest, PresignedDownloadResponse


def create_presigned_download_url(
    request: PresignedDownloadRequest,
) -> PresignedDownloadResponse:
    client = get_storage_client()
    bucket = client.bucket(request.bucket_name)
    blob = bucket.blob(request.object_name)

    signed_url = blob.generate_signed_url(
        version="v4", expiration=request.expiration_seconds, method="GET"
    )
    return PresignedDownloadResponse(presigned_url=signed_url)
