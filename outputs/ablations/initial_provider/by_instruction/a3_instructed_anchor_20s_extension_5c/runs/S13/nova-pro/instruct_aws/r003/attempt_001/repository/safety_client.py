import os
import boto3

def get_comprehend_client():
    return boto3.client('comprehend', region_name=os.getenv('AWS_REGION'))
