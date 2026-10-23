from storage_client import get_gcs_client
from storage_models import PresignedDownloadRequest, PresignedDownloadResponse


def create_presigned_download_url(
    request: PresignedDownloadRequest,
) -> PresignedDownloadResponse:
    client = get_gcs_client()
    bucket = client.bucket(request.bucket_name)
    blob = bucket.blob(request.object_name)

    url = blob.generate_signed_url(
        expiration=request.expiration_seconds,
        method="GET",
    )

    return PresignedDownloadResponse(url=url)
