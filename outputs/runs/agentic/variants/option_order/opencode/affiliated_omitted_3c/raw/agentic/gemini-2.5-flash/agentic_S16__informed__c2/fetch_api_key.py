import os
import boto3
from security_client import get_aws_secrets_manager_client


def fetch_api_key(secret_name: str) -> str:
    client = get_aws_secrets_manager_client()
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except client.exceptions.ResourceNotFoundException:
        raise ValueError(f"Secret {secret_name} not found.")
    except Exception as e:
        raise RuntimeError(f"Error fetching secret {secret_name}: {e}")

    if "SecretString" in get_secret_value_response:
        return get_secret_value_response["SecretString"]
    else:
        raise ValueError(f"Secret {secret_name} does not contain a SecretString.")
