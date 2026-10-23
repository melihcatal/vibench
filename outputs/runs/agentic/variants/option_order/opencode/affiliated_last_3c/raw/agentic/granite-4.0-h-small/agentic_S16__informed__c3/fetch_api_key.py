import os
import boto3

# AWS Secrets Manager


def fetch_api_key(secret_id: str) -> str:
    """Fetch an API key from AWS Secrets Manager.

    Returns the raw secret value as a string.
    """
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId=secret_id)
    secret = response["SecretString"]
    return secret
