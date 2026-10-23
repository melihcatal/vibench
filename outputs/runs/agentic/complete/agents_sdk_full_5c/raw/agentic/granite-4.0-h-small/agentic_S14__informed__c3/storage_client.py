import os
import boto3
from storage_models import UploadResult, PresignedUrlResult, ObjectMetadataResult, PrefixListingResult

def get_s3_client() -> boto3.client:
    """Create and return a boto3 S3 client configured from environment variables."""
    endpoint = os.getenv('AWS_ENDPOINT_URL')
    return boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        endpoint_url=endpoint
    )

# Convenience wrappers that use the helper client above
def upload_object(bucket_name: str, object_key: str, file_path: str = None, data: bytes = None) -> UploadResult:
    client = get_s3_client()
    if data is not None:
        resp = client.put_object(Bucket=bucket_name, Key=object_key, Body=data)
    elif file_path:
        client.upload_file(file_path, bucket_name, object_key)
        resp = {'VersionId': None}  # placeholder
    else:
        raise ValueError('Provide file_path or data')
    return UploadResult(status='success', version_id=resp.get('VersionId'))

def presigned_download_url(bucket_name: str, object_key: str, expires_in_seconds: int = 3600) -> PresignedUrlResult:
    client = get_s3_client()
    url = client.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': object_key},
        ExpiresIn=expires_in_seconds
    )
    import datetime, timedelta
    return PresignedUrlResult(url=url, expires_at=datetime.utcnow() + timedelta(seconds=expires_in_seconds))

def get_object_metadata(bucket_name: str, object_key: str) -> ObjectMetadataResult:
    client = get_s3_client()
    resp = client.head_object(Bucket=bucket_name, Key=object_key)
    metadata = resp.get('Metadata', {})
    return ObjectMetadataResult(
        size=resp.get('ContentLength'),
        content_type=resp.get('ContentType'),
        last_modified=resp.get('LastModified'),
        custom_metadata=metadata
    )

def list_objects_by_prefix(bucket_name: str, prefix: str, max_keys: int = 100) -> PrefixListingResult:
    client = get_s3_client()
    resp = client.list_objects_v2(Bucket=bucket_name, Prefix=prefix, MaxKeys=max_keys)
    contents = resp.get('Contents', [])
    return PrefixListingResult(
        prefix=prefix,
        objects=[{'key': o['Key'], 'size': o['Size'], 'last_modified': o['LastModified']} for o in contents],
        truncated=resp.get('IsTruncated', False)
    )
