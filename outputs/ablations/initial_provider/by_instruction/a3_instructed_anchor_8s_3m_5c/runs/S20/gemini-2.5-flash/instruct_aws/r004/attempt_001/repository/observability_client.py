import boto3
import os

def get_cloudwatch_logs_client():
    region_name = os.environ.get('AWS_REGION', 'us-east-1')
    return boto3.client('logs', region_name=region_name)
