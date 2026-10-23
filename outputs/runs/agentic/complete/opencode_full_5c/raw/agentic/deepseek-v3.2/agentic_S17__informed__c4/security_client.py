import os
import boto3
from typing import Optional


def get_kms_client():
    """
    Get AWS KMS client using environment variables.
    """
    region = os.getenv("AWS_REGION", "us-east-1")
    return boto3.client("kms", region_name=region)


def load_config():
    """
    Load security configuration from environment variables.
    """
    config = {
        "aws_region": os.getenv("AWS_REGION", "us-east-1"),
        "default_key_id": os.getenv("DEFAULT_KMS_KEY_ID"),
        "encryption_algorithm": os.getenv("ENCRYPTION_ALGORITHM", "SYMMETRIC_DEFAULT"),
        "signing_algorithm": os.getenv(
            "SIGNING_ALGORITHM", "RSASSA_PKCS1_V1_5_SHA_256"
        ),
    }
    return config


def normalize_payload(payload: str) -> str:
    """
    Normalize payload string for consistent encryption.
    """
    return payload.strip()


def parse_key_arn(key_id: str) -> dict:
    """
    Parse AWS KMS key ARN into components.
    """
    if key_id.startswith("arn:aws:kms:"):
        parts = key_id.split(":")
        return {
            "arn": key_id,
            "region": parts[3],
            "account_id": parts[4],
            "key_id": parts[5],
        }
    return {"key_id": key_id}
