import os
import boto3

def get_bedrock_client():
    return boto3.client('bedrock-runtime', region_name='us-west-2', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))