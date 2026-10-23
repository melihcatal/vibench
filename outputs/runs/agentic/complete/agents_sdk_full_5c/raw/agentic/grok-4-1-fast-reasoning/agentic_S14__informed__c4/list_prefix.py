import boto3
from typing import List

def list_prefix(
    bucket: str,
    prefix: str = ''
) -> List[str]:
    s3_client = boto3.client('s3')
    keys = []
    paginator = s3_client.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        if 'Contents' in page:
            keys.extend([obj['Key'] for obj in page['Contents']])
    return keys