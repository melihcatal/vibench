import boto3
from typing import Dict, Any

def get_object_metadata(
    bucket: str,
    key: str
) -> Dict[str, Any]:
    s3_client = boto3.client('s3')
    response = s3_client.head_object(Bucket=bucket, Key=key)
    metadata = response.pop('Metadata', {})
    return {**response, **metadata}