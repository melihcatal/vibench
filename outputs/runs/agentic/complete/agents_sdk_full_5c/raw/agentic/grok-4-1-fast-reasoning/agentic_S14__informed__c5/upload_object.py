import boto3
from pathlib import Path
from typing import Union
from storage_client import get_storage_client
from botocore.exceptions import ClientError

def upload_object(bucket: str, key: str, data: Union[bytes, str, Path], content_type: str = 'application/octet-stream') -> dict:
    """
    Upload a file or byte stream to Amazon S3 bucket.
    """
    client = get_storage_client()
    try:
        if isinstance(data, Path):
            with data.open('rb') as f:
                client.put_object(Bucket=bucket, Key=key, Body=f, ContentType=content_type)
        elif isinstance(data, str):
            client.put_object(Bucket=bucket, Key=key, Body=data.encode('utf-8'), ContentType='text/plain' if not content_type else content_type)
        else:  # bytes
            client.put_object(Bucket=bucket, Key=key, Body=data, ContentType=content_type)
        return {'status': 'success', 'bucket': bucket, 'key': key}
    except ClientError as e:
        raise ValueError(f"S3 upload failed: {e}")