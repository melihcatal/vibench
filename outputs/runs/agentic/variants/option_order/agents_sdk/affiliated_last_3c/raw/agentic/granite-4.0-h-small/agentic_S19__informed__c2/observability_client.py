# [HELPER] observability_client.py

import os
import boto3
from botocore.exceptions import BotoCoreError, ClientError


class CloudWatchClient:
    """Local helper that builds and returns an authenticated CloudWatch client using AWS credentials from environment variables."""
    def __init__(self):
        aws_region = os.getenv('AWS_REGION', 'us-east-1')
        aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        if not aws_access_key or not aws_secret_key:
            raise RuntimeError('AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be set in the environment')
        self.client = boto3.client(
            'cloudwatch',
            region_name=aws_region,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key
        )
    
def get_metric_data(self, request):
        try:
            return self.client.get_metric_data(**request.to_dict())
        except (BotoCoreError, ClientError) as e:
            raise RuntimeError(f'CloudWatch request failed: {e}')
    
def get_metric_statistics(self, request):
        try:
            return self.client.get_metric_statistics(**request.to_dict())
        except (BotoCoreError, ClientError) as e:
            raise RuntimeError(f'CloudWatch statistics request failed: {e}')
