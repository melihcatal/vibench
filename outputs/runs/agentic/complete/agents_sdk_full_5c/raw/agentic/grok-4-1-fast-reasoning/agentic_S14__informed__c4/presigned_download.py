import boto3
from typing import Optional

def presigned_download(
    bucket: str,
    key: str,
    expiration: int = 3600
) -> str:
    s3_client = boto3.client('s3')
    url = s3_client.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': bucket, 'Key': key},
        ExpiresIn=expiration
    )
    return url