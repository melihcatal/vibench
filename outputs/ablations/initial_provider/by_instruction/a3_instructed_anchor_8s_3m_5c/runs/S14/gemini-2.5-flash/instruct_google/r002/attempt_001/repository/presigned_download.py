from storage_client import get_storage_client
from storage_models import PresignedDownloadRequest, PresignedDownloadResponse

def generate_presigned_download_url(request: PresignedDownloadRequest) -> PresignedDownloadResponse:
    client = get_storage_client()
    bucket = client.bucket(request.bucket_name)
    blob = bucket.blob(request.blob_name)

    signed_url = blob.generate_signed_url(expiration=request.expiration_seconds)

    return PresignedDownloadResponse(signed_url=signed_url)
