import boto3
from datetime import timedelta
from storage_client import get_storage_client
from storage_models import PresignedDownloadRequest, PresignedDownloadResponse

def create_presigned_download_url(request: PresignedDownloadRequest) -> PresignedDownloadResponse:
    s3_client = get_storage_client()
    try:
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': request.bucket_name,
                'Key': request.object_key
            },
            ExpiresIn=int(timedelta(minutes=request.expiry_minutes).total_seconds())
        )
        return PresignedDownloadResponse(
            bucket_name=request.bucket_name,
            object_key=request.object_key,
            presigned_url=url,
            success=True
        )
    except Exception as e:
        return PresignedDownloadResponse(
            bucket_name=request.bucket_name,
            object_key=request.object_key,
            presigned_url=None,
            success=False,
            error=str(e)
        )