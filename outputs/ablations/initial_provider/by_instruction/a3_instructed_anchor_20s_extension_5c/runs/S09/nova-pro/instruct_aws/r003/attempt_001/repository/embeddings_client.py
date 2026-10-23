import os
import boto3

def get_client():
    return boto3.client('comprehend', region_name=os.getenv('AWS_REGION', 'us-west-2'))