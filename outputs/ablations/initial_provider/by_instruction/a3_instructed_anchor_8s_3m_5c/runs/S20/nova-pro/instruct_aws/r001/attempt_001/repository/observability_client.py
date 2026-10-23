import boto3
import os

def get_observability_client():
    client = boto3.client('logs', region_name=os.getenv('AWS_REGION', 'us-east-1'))
    return client