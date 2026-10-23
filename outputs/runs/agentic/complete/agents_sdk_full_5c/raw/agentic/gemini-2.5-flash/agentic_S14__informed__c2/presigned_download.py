import boto3
from storage_client import get_s3_client, get_s3_bucket_name
from storage_models import ObjectStorageDownloadRequest

def create_presigned_download_url(request: ObjectStorageDownloadRequest) -> str:
    s3_client = get_s3_client()
    bucket_name = get_s3_bucket_name()

    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': request.object_key},
            ExpiresIn=request.expiration_seconds,
        )
        return response
    except Exception as e:
        raise RuntimeError(f"Failed to create presigned URL: {e}")
