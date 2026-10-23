import boto3
import os
from typing import Optional

def get_cloudwatch_client(region: Optional[str] = None) -&gt; boto3.client:
    region = region or os.getenv('AWS_REGION', 'us-east-1')
    return boto3.client('cloudwatch', region_name=region)

def get_s3_client(region: Optional[str] = None) -&gt; boto3.client:
    region = region or os.getenv('AWS_REGION', 'us-east-1')
    return boto3.client('s3', region_name=region)
