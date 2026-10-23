import os
import boto3

def get_bedrock_client(region: str = None):
    if region is None:
        region = os.getenv('AWS_REGION', 'us-east-1')
    return boto3.client('bedrock-runtime', region_name=region)