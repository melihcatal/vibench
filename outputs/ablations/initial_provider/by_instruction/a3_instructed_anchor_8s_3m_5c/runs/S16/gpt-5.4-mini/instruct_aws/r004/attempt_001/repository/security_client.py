import os
from functools import lru_cache

import boto3


def load_secret_name(default: str) -> str:
    return os.getenv("AWS_SECRET_NAME", default)


@lru_cache(maxsize=1)
def secrets_manager_client():
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    if region:
        return boto3.client("secretsmanager", region_name=region)
    return boto3.client("secretsmanager")
