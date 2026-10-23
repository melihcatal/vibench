import boto3
import os

def get_kms_client(region: str = 'us-east-1'):
    """
    Provides a configured AWS KMS client.
    """
    return boto3.client('kms', region_name=region)

def get_cloudtrail_client(region: str = 'us-east-1'):
    """
    Provides a configured AWS CloudTrail client.
    """
    return boto3.client('cloudtrail', region_name=region)

def get_comprehend_client(region: str = 'us-east-1'):
    """
    Provides a configured AWS Comprehend client.
    """
    return boto3.client('comprehend', region_name=region)

def get_bedrock_runtime_client(region: str = 'us-east-1'):
    """
    Provides a configured AWS Bedrock Runtime client.
    """
    return boto3.client('bedrock-runtime', region_name=region)

def get_translate_client(region: str = 'us-east-1'):
    """
    Provides a configured AWS Translate client.
    """
    return boto3.client('translate', region_name=region)
