from storage_client import get_storage_client
from storage_models import PresignedDownloadRequest


def presigned_download(request: PresignedDownloadRequest):
    client = get_storage_client()
    bucket = client.bucket(request.bucket_name)
    blob = bucket.blob(request.object_name)

    url = blob.generate_signed_url(
        version="v4",
        expiration=request.expiration_seconds,
        method="GET",
    )
    return {"url": url}
