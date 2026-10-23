import boto3
from typing import Optional
from storage_client import S3_CONFIG, BUCKET_NAME

def create_presigned_download_url(
    key: str,
    expiration_seconds: int = 3600
) -> str:
    client = boto3.client('s3', **S3_CONFIG)
    url = client.generate_presigned_url(
        'get_object',
        Params={'Bucket': BUCKET_NAME, 'Key': key},
        ExpiresIn=expiration_seconds
    )
    return url
