# observability_client.py

import os
import boto3
from botocore.exceptions import NoCredentialsError

class CloudWatchClient:
    """Local helper that creates an authenticated CloudWatch client using AWS credentials."""
    def __init__(self):
        # Environment variables expected by boto3
        aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        region = os.getenv('AWS_REGION', 'us-east-1')
        
        try:
            self.client = boto3.client(
                'cloudwatch',
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_key,
                region_name=region
            )
        except NoCredentialsError:
            raise RuntimeError('AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY) are not set')