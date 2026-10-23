import os
import boto3
from botocore.config import Config

class SecurityClient:
    _kms_client = None

    @classmethod
    def get_kms_client(cls):
        if cls._kms_client is None:
            # boto3 automatically uses credentials from environment variables
            # like AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.
            region = os.environ.get("AWS_REGION", "us-east-1")
            config = Config(
                region_name=region,
                retries={
                    'max_attempts': 3,
                    'mode': 'standard'
                }
            )
            cls._kms_client = boto3.client("kms", config=config)
        return cls._kms_client

def get_kms_key_id():
    """Fetches the KMS Key ID from an environment variable."""
    key_id = os.environ.get("AWS_KMS_KEY_ID")
    if not key_id:
        raise ValueError("AWS_KMS_KEY_ID environment variable not set.")
    return key_id

def get_kms_asymmetric_key_id():
    """Fetches the Asymmetric KMS Key ID from an environment variable."""
    key_id = os.environ.get("AWS_KMS_ASYMMETRIC_KEY_ID")
    if not key_id:
        raise ValueError("AWS_KMS_ASYMMETRIC_KEY_ID environment variable not set.")
    return key_id
