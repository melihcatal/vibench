import os
import boto3


def build_secrets_client():
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
    return boto3.client("secretsmanager", region_name=region)


def normalize_secret_name(secret_id: str) -> str:
    return secret_id.strip()
