import boto3
from storage_client import get_s3_client
from storage_models import StorageConfig, DownloadRequest

def presigned_download(request: DownloadRequest, config: StorageConfig):
    s3_client = get_s3_client(config)
    url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': config.bucket, 'Key': request.object_name},
        ExpiresIn=request.expires_in
    )
    return {"presigned_url": url}
