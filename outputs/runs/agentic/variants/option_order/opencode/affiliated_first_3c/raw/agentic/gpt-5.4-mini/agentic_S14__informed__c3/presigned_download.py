from storage_client import get_s3_client
from storage_models import PresignedDownloadRequest, PresignedDownloadResponse


def presigned_download_url(bucket: str, key: str, expires_in: int = 3600, s3_client=None) -> PresignedDownloadResponse:
    client = s3_client or get_s3_client()
    request = PresignedDownloadRequest(bucket=bucket, key=key, expires_in=expires_in)
    url = client.generate_presigned_url("get_object", Params={"Bucket": request.bucket, "Key": request.key}, ExpiresIn=request.expires_in)
    return PresignedDownloadResponse(url=url, bucket=request.bucket, key=request.key, expires_in=request.expires_in)
