import boto3
from storage_client import get_s3_client
from storage_models import PresignedDownloadRequest

def create_presigned_download_url(payload: PresignedDownloadRequest, config: dict = None) -> dict:
    config = config or {}
    s3_client = get_s3_client(config)
    
    url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': config["bucket"], 'Key': payload.object_name},
        ExpiresIn=payload.expires_in
    )
    return {"presigned_url": url}
