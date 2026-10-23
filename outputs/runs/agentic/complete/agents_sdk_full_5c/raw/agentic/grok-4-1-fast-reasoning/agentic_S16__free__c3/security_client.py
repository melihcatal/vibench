import boto3
import os

def get_secrets_client() -&gt; 'boto3.client':
    region = os.getenv('AWS_REGION', 'us-east-1')
    return boto3.client('secretsmanager', region_name=region)