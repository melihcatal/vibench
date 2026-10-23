import os
from storage_client import get_s3_client
from storage_models import validate_bucket_and_key

def get_object_metadata(bucket: str, key: str):
    """Retrieve full metadata / head information for an S3 object.

    bucket: S3 bucket name
    key: object key (path)
    Returns the parsed metadata dict from boto3.
    """
    s3 = get_s3_client()
    validate_bucket_and_key(bucket, key)
    response = s3.head_object(Bucket=bucket, Key=key)
    # boto3 already returns a cleaned dict, but we keep it explicit
    return response
