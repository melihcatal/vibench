import os
from functools import lru_cache

import boto3


@lru_cache(maxsize=1)
def fetch_api_key(secret_name: str | None = None) -> str:
    secret_name = secret_name or os.environ.get("AWS_SECRET_NAME")
    if not secret_name:
        raise ValueError("AWS_SECRET_NAME is required")
    region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    client = boto3.client("secretsmanager", region_name=region)
    response = client.get_secret_value(SecretId=secret_name)
    secret = response.get("SecretString")
    if not secret:
        raise ValueError("SecretString is empty")
    return secret
