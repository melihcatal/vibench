import os
import boto3


def get_kms_client():
    return boto3.client(
        "kms",
        region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )


def get_key_arn():
    return os.getenv("KMS_KEY_ARN")


def get_asym_key_arn():
    return os.getenv("KMS_ASYM_KEY_ARN")
