"""
[HELPER] vision_client.py - Provide local configuration and client helper utilities for Static Image and Visual Understanding
"""

import boto3
import os

def get_vision_client():
    """
    Initializes and returns a Boto3 client for Amazon Rekognition.
    
    Expects AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN)
    and region (AWS_REGION) to be configured in the environment.
    """
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-1")

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError("AWS credentials are not set in environment variables.")

    return boto3.client(
        'rekognition',
        region_name=aws_region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
