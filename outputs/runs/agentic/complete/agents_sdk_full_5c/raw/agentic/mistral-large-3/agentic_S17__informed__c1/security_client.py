import os
import boto3
from botocore.client import Config
from typing import Optional

# AWS KMS integration
AWS_KMS_CONFIG = {
    'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
    'aws_secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY'),
    'region_name': os.getenv('AWS_REGION', 'us-east-1'),
    'config': Config(connect_timeout=5, read_timeout=10)
}

def get_kms_client():
    return boto3.client('kms', **AWS_KMS_CONFIG)

def get_bedrock_client():
    return boto3.client('bedrock-runtime', **AWS_KMS_CONFIG)

def get_comprehend_client():
    return boto3.client('comprehend', **AWS_KMS_CONFIG)

def get_translate_client():
    return boto3.client('translate', **AWS_KMS_CONFIG)