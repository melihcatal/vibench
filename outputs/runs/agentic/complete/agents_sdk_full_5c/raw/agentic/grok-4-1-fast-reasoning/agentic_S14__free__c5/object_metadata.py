import boto3
import os
from typing import Dict, Any, Optional

def object_metadata(
    bucket: str,
    key: str,
    region: str = 'us-east-1'
) -> Dict[str, Any]:
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=region
    )
    resp = s3.head_object(Bucket=bucket, Key=key)
    return dict(resp)
