import os
import boto3

def get_cloudwatch_client():
    return boto3.client('cloudwatch', region_name=os.getenv('AWS_REGION', 'us-west-2'))

def get_s3_client():
    return boto3.client('s3', region_name=os.getenv('AWS_REGION', 'us-west-2'))