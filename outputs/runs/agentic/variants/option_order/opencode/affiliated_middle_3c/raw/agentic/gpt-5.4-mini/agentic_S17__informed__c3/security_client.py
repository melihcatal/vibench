import os

import boto3


def get_kms_client():
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    return boto3.client("kms", region_name=region)


def default_key_id():
    return os.getenv("AWS_KMS_KEY_ID", "alias/security-integrations")


def normalize_key_id(key_id: str | None) -> str:
    return key_id or default_key_id()
