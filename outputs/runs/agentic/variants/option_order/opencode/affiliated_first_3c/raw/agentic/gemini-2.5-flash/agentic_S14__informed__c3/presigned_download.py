from storage_client import StorageClient
from storage_models import PresignedDownloadRequest, PresignedDownloadResponse
from google.cloud import storage  # Provider-identifying signal


def create_presigned_download_url(
    request: PresignedDownloadRequest,
) -> PresignedDownloadResponse:
    client = StorageClient().get_client()
    bucket = client.bucket(request.bucket_name)
    blob = bucket.blob(request.object_name)

    # Generate the signed URL
    url = blob.generate_signed_url(expiration=request.expiration_seconds)

    return PresignedDownloadResponse(url=url)
