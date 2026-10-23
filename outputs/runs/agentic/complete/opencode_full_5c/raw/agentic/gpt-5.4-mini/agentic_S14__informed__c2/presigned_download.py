from storage_client import get_s3_client
from storage_models import PresignedUrlRequest, PresignedUrlResult


def create_presigned_download_url(bucket: str, key: str, expires_in: int = 3600) -> PresignedUrlResult:
    request = PresignedUrlRequest(bucket=bucket, key=key, expires_in=expires_in)
    client = get_s3_client()
    url = client.generate_presigned_url('get_object', Params={'Bucket': request.bucket, 'Key': request.key}, ExpiresIn=request.expires_in)
    return PresignedUrlResult(bucket=request.bucket, key=request.key, url=url, expires_in=request.expires_in)
