import os
import boto3

def get_client():
    return boto3.client('cloudwatch', region_name=os.getenv('AWS_REGION'))