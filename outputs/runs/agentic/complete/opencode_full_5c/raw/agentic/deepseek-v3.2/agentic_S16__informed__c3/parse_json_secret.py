import os
import json
import boto3
from botocore.exceptions import ClientError
from typing import Any, Dict


def parse_json_secret(secret_name: str) -> Dict[str, Any]:
    """
    Retrieve and parse a JSON-formatted secret from AWS Secrets Manager.

    Args:
        secret_name: Name of the JSON secret in AWS Secrets Manager

    Returns:
        Parsed JSON data as a dictionary
    """
    # AWS provider-specific client
    client = boto3.client(
        "secretsmanager", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    try:
        response = client.get_secret_value(SecretId=secret_name)
        if "SecretString" in response:
            secret_string = response["SecretString"]
            try:
                parsed_data = json.loads(secret_string)
                if not isinstance(parsed_data, dict):
                    raise ValueError(f"Secret {secret_name} is not a JSON object")
                return parsed_data
            except json.JSONDecodeError as e:
                raise ValueError(
                    f"Secret {secret_name} contains invalid JSON: {e}"
                ) from e
        else:
            raise ValueError(f"Secret {secret_name} is not a string")
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "ResourceNotFoundException":
            raise ValueError(f"JSON secret {secret_name} not found") from e
        elif error_code == "InvalidRequestException":
            raise ValueError(f"Invalid request for JSON secret {secret_name}") from e
        else:
            raise RuntimeError(
                f"Error retrieving JSON secret {secret_name}: {e}"
            ) from e
