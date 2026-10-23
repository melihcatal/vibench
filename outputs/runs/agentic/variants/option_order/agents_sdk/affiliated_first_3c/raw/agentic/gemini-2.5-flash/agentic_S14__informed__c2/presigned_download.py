
from storage_client import get_s3_client
from storage_models import PresignedDownloadRequest, PresignedDownloadResponse

def create_presigned_download_url(request: PresignedDownloadRequest) -> PresignedDownloadResponse:
    s3_client = get_s3_client()

    url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': request.bucket_name,
                'Key': request.object_key},
        ExpiresIn=request.expiration_seconds
    )

    return PresignedDownloadResponse(url=url)
