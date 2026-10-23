import os
from typing import Optional

import boto3


def fetch_api_key(secret_id: Optional[str] = None, region_name: Optional[str] = None) -> str:
    secret_id = secret_id or os.environ.get("AWS_SECRET_ID") or os.environ.get("API_KEY_SECRET_ID")
    if not secret_id:
        raise ValueError("Missing secret identifier")
    client = boto3.client("secretsmanager", region_name=region_name or os.environ.get("AWS_REGION"))
    response = client.get_secret_value(SecretId=secret_id)
    secret_string = response.get("SecretString")
    if secret_string is None:
        secret_binary = response.get("SecretBinary")
        if secret_binary is None:
            raise ValueError("Secret contains no retrievable value")
        secret_string = secret_binary.decode("utf-8")
    return secret_string


if __name__ == "__main__":
    print(fetch_api_key())
