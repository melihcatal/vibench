import os
import boto3
from botocore.config import Config

def get_kms_client():
    """
    Initializes and returns a Boto3 KMS client.
    Configuration is loaded from environment variables.
    """
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    
    config = Config(
        region_name=aws_region,
        retries={
            'max_attempts': 3,
            'mode': 'standard'
        }
    )
    
    return boto3.client("kms", config=config)

def get_key_id():
    """
    Retrieves the KMS Key ID from an environment variable.
    """
    key_id = os.environ.get("AWS_KMS_KEY_ID")
    if not key_id:
        raise ValueError("AWS_KMS_KEY_ID environment variable not set.")
    return key_id

def get_asymmetric_key_id():
    """
    Retrieves the Asymmetric KMS Key ID from an environment variable.
    """
    key_id = os.environ.get("AWS_KMS_ASYMMETRIC_SIGNING_KEY_ID")
    if not key_id:
        raise ValueError("AWS_KMS_ASYMMETRIC_SIGNING_KEY_ID environment variable not set.")
    return key_id
