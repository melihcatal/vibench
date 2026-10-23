import os

import boto3


def get_bedrock_client(config=None):
    config = config or {}
    region_name = config.get("region", "us-east-1")
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID", config.get("aws_access_key_id"))
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY", config.get("aws_secret_access_key"))
    client = boto3.client("bedrock-runtime", region_name=region_name,
        aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    return client