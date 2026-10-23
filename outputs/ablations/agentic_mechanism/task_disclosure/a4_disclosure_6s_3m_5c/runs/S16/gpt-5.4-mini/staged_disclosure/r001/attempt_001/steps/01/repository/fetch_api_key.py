import os
from typing import Optional

import boto3


def fetch_api_key(secret_name: str, region_name: Optional[str] = None) -> str:
    session = boto3.session.Session(region_name=region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))
    client = session.client("secretsmanager")
    response = client.get_secret_value(SecretId=secret_name)
    if "SecretString" in response and response["SecretString"] is not None:
        return response["SecretString"]
    secret_binary = response.get("SecretBinary")
    if secret_binary is None:
        raise ValueError("Secret value is empty")
    return secret_binary.decode("utf-8")
