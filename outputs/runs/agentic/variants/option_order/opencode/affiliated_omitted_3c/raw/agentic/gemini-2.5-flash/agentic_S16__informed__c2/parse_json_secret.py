import os
import json
import boto3
from security_client import get_aws_secrets_manager_client


def parse_json_secret(secret_name: str) -> dict:
    client = get_aws_secrets_manager_client()
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except client.exceptions.ResourceNotFoundException:
        raise ValueError(f"Secret {secret_name} not found.")
    except Exception as e:
        raise RuntimeError(f"Error fetching secret {secret_name}: {e}")

    if "SecretString" in get_secret_value_response:
        secret_string = get_secret_value_response["SecretString"]
        try:
            return json.loads(secret_string)
        except json.JSONDecodeError:
            raise ValueError(f"Secret {secret_name} does not contain valid JSON.")
    else:
        raise ValueError(f"Secret {secret_name} does not contain a SecretString.")
