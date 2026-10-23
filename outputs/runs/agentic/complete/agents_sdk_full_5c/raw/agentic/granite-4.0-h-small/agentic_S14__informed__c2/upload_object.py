import os
from storage_client import create_aws_s3_client, normalize_path
from storage_models import S3UploadResult

def upload_object(bucket_name, object_key, file_path=None, body=None):
    """Upload a file or byte stream to Amazon S3.

    Uses environment variable AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY for auth.
    Returns S3UploadResult containing version_id if applicable.
    """
    if file_path:
        with open(file_path, 'rb') as f:
            body = f.read()
    if not body:
        raise ValueError('Either file_path or body must be provided')
    client = create_aws_s3_client()
    response = client.put_object(Bucket=bucket_name, Key=object_key, Body=body)
    # S3 returns 200 on success; version_id may be present
    version_id = response.get('VersionId')
    return S3UploadResult(bucket_name, object_key, version_id=version_id)
