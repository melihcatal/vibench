from storage_client import get_bucket
from storage_models import PresignedDownloadRequest, PresignedDownloadResponse


def presigned_download(bucket_name: str, object_name: str, expires_in: int = 3600) -> PresignedDownloadResponse:
    bucket = get_bucket(bucket_name)
    req = PresignedDownloadRequest(object_name=object_name, expires_in=expires_in)
    blob = bucket.blob(req.object_name)
    url = blob.generate_signed_url(expiration=req.expires_in, method='GET', version='v4')
    return PresignedDownloadResponse(bucket_name=bucket_name, object_name=object_name, url=url, expires_in=req.expires_in)
