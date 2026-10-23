import os
import boto3
from botocore.exceptions import NoCredentialsError

def get_s3_client():
    """Create and cache a boto3 S3 client using environment credentials.
    AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are read from os.environ.
    Returns a ready-to-use client object.
    """
    try:
        client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
        return client
    except NoCredentialsError:
        raise RuntimeError('Missing AWS credentials. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.')
