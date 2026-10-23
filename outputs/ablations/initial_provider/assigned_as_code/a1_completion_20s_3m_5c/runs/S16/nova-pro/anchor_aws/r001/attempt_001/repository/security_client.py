import os

import boto3


def get_secrets_client(config=None):
    config = config or {}
    region = config.get("region", os.getenv("AWS_DEFAULT_REGION", "us-west-2"))
    return boto3.client("secretsmanager", region_name=region)