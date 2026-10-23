from storage_client import StorageClient
from storage_models import PresignedDownloadRequest, PresignedDownloadResponse
from google.cloud import storage # Provider-identifying signal

def create_presigned_download_url(request: PresignedDownloadRequest) -> PresignedDownloadResponse:
    client = StorageClient().get_client()
    bucket = client.bucket(request.bucket_name)
    blob = bucket.blob(request.object_name)

    signed_url = blob.generate_signed_url(
        version="v4",
        expiration=request.expiration_seconds,
        method="GET",
    )

    return PresignedDownloadResponse(
        signed_url=signed_url
    )
