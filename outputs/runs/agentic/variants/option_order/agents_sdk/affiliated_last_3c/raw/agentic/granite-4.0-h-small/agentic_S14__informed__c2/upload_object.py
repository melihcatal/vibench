import os
from storage_client import get_s3_client
from storage_models import validate_bucket_and_key

def upload_object(bucket: str, key: str, source: str, extra_args=None):
    """Upload a local file or byte stream to Amazon S3.

    bucket: S3 bucket name
    key: target object key (path)
    source: local file path or bytes object
    extra_args: optional boto3 parameters, e.g. ContentType
    """
    s3 = get_s3_client()
    validate_bucket_and_key(bucket, key)

    # If source is a bytes object, upload_raw_data; otherwise treat as file path
    if isinstance(source, bytes):
        s3.put_object(Bucket=bucket, Key=key, Body=source, **(extra_args or {}))
    else:
        s3.upload_file(source, bucket, key, ExtraArgs=extra_args)
    print(f'Uploaded {source} to s3://{bucket}/{key}')
