import boto3

from storage_client import default_bucket, s3_client
from storage_models import normalize_body, normalize_key, response_payload


def upload_object(bucket=None, key=None, body=None, content_type=None, metadata=None):
    bucket_name = default_bucket(bucket)
    object_key = normalize_key(key)
    payload = normalize_body(body)
    client = s3_client()
    params = {"Bucket": bucket_name, "Key": object_key, "Body": payload}
    if content_type:
        params["ContentType"] = content_type
    if metadata:
        params["Metadata"] = dict(metadata)
    result = client.put_object(**params)
    return response_payload(
        provider="aws",
        service="s3",
        bucket=bucket_name,
        key=object_key,
        etag=result.get("ETag"),
        version_id=result.get("VersionId"),
    )
