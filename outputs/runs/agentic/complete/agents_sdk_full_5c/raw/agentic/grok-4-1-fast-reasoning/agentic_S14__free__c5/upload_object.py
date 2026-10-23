import boto3
import os
from typing import Union, Optional
from pathlib import Path

def upload_object(
    bucket: str,
    key: str,
    data: Union[bytes, str, Path],
    content_type: Optional[str] = None,
    region: str = 'us-east-1'
):
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=region
    )
    if isinstance(data, Path):
        body = data.read_bytes()
    elif isinstance(data, str):
        body = data.encode('utf-8')
    else:
        body = data
    extra_args = {}
    if content_type:
        extra_args['ContentType'] = content_type
    s3.put_object(Bucket=bucket, Key=key, Body=body, **extra_args)
