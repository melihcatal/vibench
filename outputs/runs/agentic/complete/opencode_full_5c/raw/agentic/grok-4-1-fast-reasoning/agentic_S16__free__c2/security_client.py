import os
import boto3


def get_secrets_client():
    region = os.getenv("AWS_REGION", "us-east-1")
    return boto3.client("secretsmanager", region_name=region)
