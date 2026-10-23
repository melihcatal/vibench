import boto3
from typing import Optional, Dict, Any

def upload_object(
    bucket: str,
    key: str,
    data: bytes,
    content_type: Optional[str] = None
) -> Dict[str, Any]:
    s3_client = boto3.client('s3')
    extra_args = {}
    if content_type:
        extra_args['ContentType'] = content_type
    s3_client.put_object(
        Bucket=bucket,
        Key=key,
        Body=data,
        **extra_args
    )
    return {'bucket': bucket, 'key': key, 'location': f's3://{bucket}/{key}'}