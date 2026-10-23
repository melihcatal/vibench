from storage_client import get_s3_client
from storage_models import PresignedDownloadRequest, PresignedDownloadResponse

def presigned_download(request: PresignedDownloadRequest) -> PresignedDownloadResponse:
    s3_client = get_s3_client()

    url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': request.bucket_name, 'Key': request.object_name},
        ExpiresIn=request.expires_in
    )

    return PresignedDownloadResponse(url=url)
