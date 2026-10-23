import boto3
import json
import os
from typing import Dict, Any
from botocore.exceptions import ClientError


def parse_json_secret(secret_name: str) -> Dict[str, Any]:
    """
    Retrieve and parse a JSON-formatted secret from AWS Secrets Manager.

    Args:
        secret_name: Name of the secret in AWS Secrets Manager

    Returns:
        Parsed JSON content as a dictionary
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        response = client.get_secret_value(SecretId=secret_name)

        if "SecretString" in response:
            secret_string = response["SecretString"]
            try:
                parsed_data = json.loads(secret_string)
                return parsed_data
            except json.JSONDecodeError as e:
                raise ValueError(f"Secret content is not valid JSON: {e}")
        elif "SecretBinary" in response:
            secret_binary = response["SecretBinary"]
            try:
                secret_string = secret_binary.decode("utf-8")
                parsed_data = json.loads(secret_string)
                return parsed_data
            except (UnicodeDecodeError, json.JSONDecodeError) as e:
                raise ValueError(
                    f"Failed to decode or parse binary secret as JSON: {e}"
                )
        else:
            raise ValueError("Secret has neither SecretString nor SecretBinary")

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "ResourceNotFoundException":
            raise Exception(f"Secret '{secret_name}' not found in AWS Secrets Manager")
        elif error_code == "AccessDeniedException":
            raise Exception(f"Access denied to secret '{secret_name}'")
        elif error_code == "DecryptionFailure":
            raise Exception(f"Failed to decrypt secret '{secret_name}'")
        else:
            raise Exception(f"AWS Secrets Manager error: {e}")


def get_nested_value(secret_name: str, key_path: str, default: Any = None) -> Any:
    """
    Retrieve a specific nested value from a JSON secret.

    Args:
        secret_name: Name of the secret
        key_path: Dot-separated path to the nested key (e.g., 'api.keys.production')
        default: Default value if key not found

    Returns:
        The value at the specified key path
    """
    secret_data = parse_json_secret(secret_name)

    keys = key_path.split(".")
    current = secret_data

    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default

    return current


if __name__ == "__main__":
    config = parse_json_secret("prod/app-config")
    print(f"Config keys: {list(config.keys())}")

    api_key = get_nested_value("prod/app-config", "api.keys.production")
    print(f"Production API key: {api_key[:8]}...")
