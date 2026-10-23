import os
from storage_client import get_s3_client, S3_BUCKET_NAME
from storage_models import PresignedDownloadRequest, PresignedDownloadResponse

def create_presigned_download_url(request: PresignedDownloadRequest) -> PresignedDownloadResponse:
    s3_client = get_s3_client()
    
    try:
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': S3_BUCKET_NAME, 'Key': request.object_key},
            ExpiresIn=request.expires_in_seconds
        )
        return PresignedDownloadResponse(success=True, url=url, object_key=request.object_key)
    except Exception as e:
        return PresignedDownloadResponse(success=False, error_message=str(e))
