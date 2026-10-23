import boto3
import os
from typing import List, Optional

def list_prefix(
    bucket: str,
    prefix: str,
    region: str = 'us-east-1'
) -> List[str]:
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=region
    )
    paginator = s3.get_paginator('list_objects_v2')
    keys = []
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        if 'Contents' in page:
            keys.extend(obj['Key'] for obj in page['Contents'])
    return keys
