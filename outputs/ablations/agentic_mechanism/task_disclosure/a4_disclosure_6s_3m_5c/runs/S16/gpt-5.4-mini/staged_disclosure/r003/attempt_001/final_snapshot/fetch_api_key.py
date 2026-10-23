import os

import boto3


def fetch_api_key(secret_id: str | None = None) -> str:
    secret_name = secret_id or os.environ.get("AWS_SECRETS_MANAGER_SECRET_ID")
    if not secret_name:
        raise ValueError("AWS_SECRETS_MANAGER_SECRET_ID is required")

    region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    client_kwargs = {}
    if region:
        client_kwargs["region_name"] = region

    client = boto3.client("secretsmanager", **client_kwargs)
    response = client.get_secret_value(SecretId=secret_name)

    if "SecretString" in response and response["SecretString"] is not None:
        return response["SecretString"]

    secret_binary = response.get("SecretBinary")
    if secret_binary is not None:
        return secret_binary.decode("utf-8")

    raise RuntimeError("Secret value was empty")
