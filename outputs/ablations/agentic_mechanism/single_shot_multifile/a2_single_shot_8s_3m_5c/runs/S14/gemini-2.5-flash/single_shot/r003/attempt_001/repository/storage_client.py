import os
import boto3

def get_s3_client():
    return boto3.client(
        's3',
        region_name=os.environ.get('AWS_REGION', 'us-east-1')
    )

def get_textract_client():
    return boto3.client(
        'textract',
        region_name=os.environ.get('AWS_REGION', 'us-east-1')
    )

def get_translate_client():
    return boto3.client(
        'translate',
        region_name=os.environ.get('AWS_REGION', 'us-east-1')
    )

def get_bedrock_runtime_client():
    return boto3.client(
        'bedrock-runtime',
        region_name=os.environ.get('AWS_REGION', 'us-east-1')
    )
