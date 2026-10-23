import os
from functools import lru_cache
import boto3


def resolve_bucket_name(bucket: str | None = None) -> str:
    if bucket:
        return bucket
    env_bucket = os.getenv('AWS_S3_BUCKET') or os.getenv('S3_BUCKET')
    if not env_bucket:
        raise ValueError('bucket is required')
    return env_bucket


@lru_cache(maxsize=1)
def get_s3_client():
    region = os.getenv('AWS_REGION') or os.getenv('AWS_DEFAULT_REGION')
    if region:
        return boto3.client('s3', region_name=region)
    return boto3.client('s3')
