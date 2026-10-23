import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from typing import Optional

def get_storage_client(region_name: Optional[str] = None) -&gt; boto3.client:
    """
    Get AWS S3 client using boto3.
    Auth via AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY env vars or IAM roles.
    """
    try:
        return boto3.client('s3', region_name=region_name)
    except NoCredentialsError:
        raise ValueError("AWS credentials not configured.")