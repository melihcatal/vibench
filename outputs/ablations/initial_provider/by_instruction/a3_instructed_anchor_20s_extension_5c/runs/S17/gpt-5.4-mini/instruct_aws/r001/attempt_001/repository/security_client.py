import os

import boto3


def get_region() -> str:
    return os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1"))


def get_key_id() -> str:
    return os.environ.get("AWS_KMS_KEY_ID", "alias/default-security-key")


def get_kms_client():
    return boto3.client("kms", region_name=get_region())
