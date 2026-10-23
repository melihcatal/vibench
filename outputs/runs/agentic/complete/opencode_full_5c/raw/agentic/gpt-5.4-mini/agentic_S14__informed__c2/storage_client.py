import os

import boto3


def get_s3_client():
    endpoint_url = os.getenv('AWS_S3_ENDPOINT_URL')
    region_name = os.getenv('AWS_REGION') or os.getenv('AWS_DEFAULT_REGION') or 'us-east-1'
    return boto3.client('s3', endpoint_url=endpoint_url, region_name=region_name)


def get_bucket_name(default: str = '') -> str:
    return os.getenv('S3_BUCKET_NAME', default)
