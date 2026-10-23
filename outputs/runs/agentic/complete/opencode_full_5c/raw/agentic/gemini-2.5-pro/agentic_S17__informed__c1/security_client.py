import os
import boto3


def get_kms_client():
    return boto3.client("kms", region_name=os.environ.get("AWS_REGION", "us-east-1"))


def get_key_id():
    key_id = os.environ.get("KMS_KEY_ID")
    if not key_id:
        raise ValueError("KMS_KEY_ID environment variable not set.")
    return key_id
