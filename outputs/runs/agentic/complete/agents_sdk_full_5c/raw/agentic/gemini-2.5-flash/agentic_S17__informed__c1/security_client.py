"""
security_client.py - Provide local configuration and client helper utilities for Key Management and Encryption
"""
import os
import boto3

def get_kms_client():
    """
    Returns a configured AWS KMS client.
    Requires AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_REGION environment variables.
    """
    return boto3.client(
        'kms',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
        region_name=os.environ.get('AWS_REGION', 'us-east-1') # Default region if not specified
    )

def get_comprehend_client():
    """
    Returns a configured AWS Comprehend client.
    """
    return boto3.client(
        'comprehend',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
        region_name=os.environ.get('AWS_REGION', 'us-east-1')
    )

def get_bedrock_runtime_client():
    """
    Returns a configured AWS Bedrock Runtime client.
    """
    return boto3.client(
        'bedrock-runtime',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
        region_name=os.environ.get('AWS_REGION', 'us-east-1')
    )

def get_translate_client():
    """
    Returns a configured AWS Translate client.
    """
    return boto3.client(
        'translate',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
        region_name=os.environ.get('AWS_REGION', 'us-east-1')
    )

def get_cloudtrail_client():
    """
    Returns a configured AWS CloudTrail client.
    """
    return boto3.client(
        'cloudtrail',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
        region_name=os.environ.get('AWS_REGION', 'us-east-1')
    )
