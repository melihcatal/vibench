import boto3
from botocore.exceptions import ClientError
from typing import Dict, Any

from storage_client import get_aws_credentials

def get_object_metadata(
    bucket: str,
    key: str
) -> Dict[str, Any]:
    creds = get_aws_credentials()
    s3_client = boto3.client('s3', **creds)
    
    try:
        metadata = s3_client.head_object(
            Bucket=bucket,
            Key=key
        )
        return dict(metadata)
    except ClientError as e:
        raise RuntimeError(f"S3 head_object failed: {e}") from e
