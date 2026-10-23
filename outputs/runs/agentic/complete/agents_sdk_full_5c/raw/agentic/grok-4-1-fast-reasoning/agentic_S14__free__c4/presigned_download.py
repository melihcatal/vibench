import boto3
from storage_client import get_aws_creds

def presigned_download(bucket: str, key: str, expiration: int = 3600) -> str:
    s3 = boto3.client('s3', **get_aws_creds())
    url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket, 'Key': key},
        ExpiresIn=expiration
    )
    return url