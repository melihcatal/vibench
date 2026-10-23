import os
import boto3


def get_region() -> str:
    return os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))


def get_sns_client():
    return boto3.client("sns", region_name=get_region())


def get_sqs_client():
    return boto3.client("sqs", region_name=get_region())


def get_s3_client():
    return boto3.client("s3", region_name=get_region())


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"missing environment variable: {name}")
    return value
