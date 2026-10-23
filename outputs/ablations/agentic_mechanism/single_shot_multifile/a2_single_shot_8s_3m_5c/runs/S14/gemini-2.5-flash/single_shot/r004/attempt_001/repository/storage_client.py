import os
import boto3
from botocore.exceptions import NoCredentialsError

_s3_client = None

def get_s3_client():
    global _s3_client
    if _s3_client is None:
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        aws_region = os.getenv('AWS_REGION')

        if not all([aws_access_key_id, aws_secret_access_key, aws_region]):
            raise NoCredentialsError(
                "AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION) not found in environment."
            )
        _s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region
        )
    return _s3_client

def get_s3_bucket_name() -> str:
    bucket_name = os.getenv('S3_BUCKET_NAME')
    if not bucket_name:
        raise ValueError("S3_BUCKET_NAME environment variable not set.")
    return bucket_name
