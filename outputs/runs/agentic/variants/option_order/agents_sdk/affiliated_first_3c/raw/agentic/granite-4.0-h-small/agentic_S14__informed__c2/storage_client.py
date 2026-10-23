import os
import boto3
from botocore.exceptions import NoCredentialsError

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

if not (AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY):
    raise RuntimeError('AWS credentials not found in environment variables')

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

def get_s3_client() -> boto3.client:
    """Return the pre‑configured S3 client."""
    return s3_client