import os
from typing import Optional

import boto3


def fetch_api_key(secret_id: Optional[str] = None, region_name: Optional[str] = None) -> str:
    secret_name = secret_id or os.environ.get("AWS_SECRET_ID") or os.environ.get("API_KEY_SECRET_ID")
    if not secret_name:
        raise ValueError("Missing secret identifier")
    session = boto3.session.Session(region_name=region_name or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION"))
    client = session.client("secretsmanager")
    response = client.get_secret_value(SecretId=secret_name)
    secret_string = response.get("SecretString")
    if secret_string is None:
        raise ValueError("Secret does not contain a string value")
    return secret_string


if __name__ == "__main__":
    print(fetch_api_key())
