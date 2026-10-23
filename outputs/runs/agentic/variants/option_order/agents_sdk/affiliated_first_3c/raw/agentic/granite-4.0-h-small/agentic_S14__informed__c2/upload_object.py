import os
from storage_client import get_s3_client
from storage_models import validate_bucket_name

def upload_object(bucket: str, key: str, body):
    """Upload a file/object to Amazon S3.
    Args:
        bucket (str): Bucket name.
        key (str): Object key (path) within the bucket.
        body (bytes/str/IO): File content or file-like object.
    """
    if not validate_bucket_name(bucket):
        raise ValueError("Invalid bucket name")
    s3 = get_s3_client()
    if isinstance(body, (bytes, str)):
        body = body.encode() if isinstance(body, str) else body
    s3.put_object(Bucket=bucket, Key=key, Body=body)
    print(f"Uploaded {key} to bucket {bucket}")