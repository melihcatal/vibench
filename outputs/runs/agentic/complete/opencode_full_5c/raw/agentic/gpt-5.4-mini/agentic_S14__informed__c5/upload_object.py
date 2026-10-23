import boto3

from storage_client import get_bucket_name, get_s3_client
from storage_models import UploadResult, normalize_bytes


def upload_object(bucket=None, key=None, body=None, content_type=None, metadata=None):
    client = get_s3_client()
    bucket_name = get_bucket_name(bucket)
    payload = normalize_bytes(body)
    extra = {}
    if content_type:
        extra["ContentType"] = content_type
    if metadata:
        extra["Metadata"] = metadata
    response = client.put_object(Bucket=bucket_name, Key=key, Body=payload, **extra)
    return UploadResult(
        bucket=bucket_name,
        key=key,
        etag=response.get("ETag"),
        version_id=response.get("VersionId"),
    )
