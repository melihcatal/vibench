import boto3
from typing import Union
from pathlib import Path
from storage_client import get_aws_creds

def upload_object(bucket: str, key: str, data: Union[bytes, Path]) -> str:
    s3 = boto3.client('s3', **get_aws_creds())
    if isinstance(data, Path):
        with data.open('rb') as f:
            resp = s3.put_object(Bucket=bucket, Key=key, Body=f)
    elif isinstance(data, bytes):
        resp = s3.put_object(Bucket=bucket, Key=key, Body=data)
    else:
        raise ValueError("data must be bytes or Path")
    return resp['ETag']