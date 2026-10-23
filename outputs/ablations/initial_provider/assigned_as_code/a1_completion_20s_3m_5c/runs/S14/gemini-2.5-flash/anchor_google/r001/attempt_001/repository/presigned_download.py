from datetime import timedelta

from storage_client import get_storage_client, get_bucket_name, get_project_id
from storage_models import PresignedDownloadRequest, PresignedDownloadResponse

def presigned_download(payload: PresignedDownloadRequest):
    client = get_storage_client(get_project_id())
    bucket = client.bucket(get_bucket_name())
    blob = bucket.blob(payload.object_name)

    # Generate a v4 signed URL for downloading the blob.
    # The URL will be valid for 1 hour by default.
    url = blob.generate_signed_url(
        version="v4",
        expiration=timedelta(seconds=payload.expiration_seconds),
        method="GET",
    )

    return PresignedDownloadResponse(url=url)
