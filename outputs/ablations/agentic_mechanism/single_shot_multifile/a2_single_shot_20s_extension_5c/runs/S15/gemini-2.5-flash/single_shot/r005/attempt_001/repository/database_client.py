import os
import boto3

def get_dynamodb_client():
    aws_region = os.environ.get('AWS_REGION', 'us-east-1')
    return boto3.client('dynamodb', region_name=aws_region)

def get_bedrock_client():
    aws_region = os.environ.get('AWS_REGION', 'us-east-1')
    return boto3.client('bedrock-runtime', region_name=aws_region)

def get_comprehend_client():
    aws_region = os.environ.get('AWS_REGION', 'us-east-1')
    return boto3.client('comprehend', region_name=aws_region)

def get_translate_client():
    aws_region = os.environ.get('AWS_REGION', 'us-east-1')
    return boto3.client('translate', region_name=aws_region)

def get_s3_client():
    aws_region = os.environ.get('AWS_REGION', 'us-east-1')
    return boto3.client('s3', region_name=aws_region)
