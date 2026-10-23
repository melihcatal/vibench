import os
import boto3
from botocore.exceptions import ClientError
from typing import Union, Dict, Any

from storage_client import get_aws_credentials

def upload_object(
    bucket: str,
    key: str,
    data: Union[bytes, str],
    content_type: str = "application/octet-stream"
) -> Dict[str, Any]:
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    creds = get_aws_credentials()
    s3_client = boto3.client('s3', **creds)
    
    try:
        response = s3_client.put_object(
            Bucket=bucket,
            Key=key,
            Body=data,
            ContentType=content_type
        )
        return {
            "bucket": bucket,
            "key": key,
            "etag": response.get("ETag"),
            "version_id": response.get("VersionId")
        }
    except ClientError as e:
        raise RuntimeError(f"S3 upload failed: {e}") from e
