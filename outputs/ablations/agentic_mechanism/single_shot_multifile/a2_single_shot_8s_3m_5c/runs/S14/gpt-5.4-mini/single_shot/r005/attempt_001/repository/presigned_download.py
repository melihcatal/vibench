from storage_client import get_s3_client, resolve_bucket_name
from storage_models import PresignedDownloadRequest, PresignedDownloadResponse


def presigned_download(request: PresignedDownloadRequest) -> PresignedDownloadResponse:
    s3 = get_s3_client()
    bucket = resolve_bucket_name(request.bucket)
    params = {'Bucket': bucket, 'Key': request.key}
    url = s3.generate_presigned_url('get_object', Params=params, ExpiresIn=request.expires_in)
    return PresignedDownloadResponse(url=url, expires_in=request.expires_in)
