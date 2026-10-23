import os
import boto3
from storage_client import get_s3_client
from storage_models import PresignedDownloadRequest, PresignedDownloadResponse

def create_presigned_download_url(request: PresignedDownloadRequest) -> PresignedDownloadResponse:
    s3_client = get_s3_client()

    # AWS S3 `generate_presigned_url` is used here
    url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': request.bucket, 'Key': request.key},
        ExpiresIn=request.expires_in
    )

    return PresignedDownloadResponse(url=url)
