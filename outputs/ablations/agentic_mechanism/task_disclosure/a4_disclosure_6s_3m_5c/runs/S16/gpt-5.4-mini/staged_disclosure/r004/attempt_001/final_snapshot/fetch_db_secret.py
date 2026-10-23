import os
from typing import Optional

import boto3


def fetch_db_secret(secret_id: Optional[str] = None, region_name: Optional[str] = None) -> str:
    secret_name = secret_id or os.environ["AWS_SECRET_NAME"]
    region = region_name or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    client = boto3.client("secretsmanager", region_name=region)
    response = client.get_secret_value(SecretId=secret_name)
    if "SecretString" in response and response["SecretString"] is not None:
        return response["SecretString"]
    secret_binary = response.get("SecretBinary")
    if secret_binary is None:
        raise ValueError("Secret value is empty")
    return secret_binary.decode("utf-8")


if __name__ == "__main__":
    print(fetch_db_secret())
