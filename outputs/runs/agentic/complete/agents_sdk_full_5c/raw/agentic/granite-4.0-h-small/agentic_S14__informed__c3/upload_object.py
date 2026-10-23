import os
import boto3
from storage_models import UploadResult

def upload_object(bucket_name: str, object_key: str, file_path: str = None, data: bytes = None) -> UploadResult:
    """Upload a file or raw bytes to an S3 bucket.

    Uses AWS S3 via boto3 SDK. Credentials are read from environment variables
    AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.
    """
    s3 = boto3.client('s3')
    if data is not None:
        response = s3.put_object(Bucket=bucket_name, Key=object_key, Body=data)
    elif file_path:
        response = s3.upload_file(file_path, bucket_name, object_key)
    else:
        raise ValueError('Either file_path or data must be provided')
    return UploadResult(status='success', version_id=response.get('VersionId'))
