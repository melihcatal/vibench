import os
from botocore.client import Config

def get_s3_client():
    """Return a configured boto3 S3 client using environment variables for credentials and region."""
    aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    region = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    if not aws_access_key or not aws_secret_key:
        raise RuntimeError('AWS credentials not provided in environment.')
    config = Config(signature_version='s3v4', region_name=region)
    return boto3.client(
        's3',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        config=config
    )