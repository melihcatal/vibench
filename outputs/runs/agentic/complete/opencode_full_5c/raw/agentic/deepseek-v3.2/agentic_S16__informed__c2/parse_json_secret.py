import os
import json
import boto3
from botocore.exceptions import ClientError
from typing import Any, Dict


def parse_json_secret(secret_name: str) -> Dict[str, Any]:
    """
    Retrieve and parse a JSON-formatted secret from AWS Secrets Manager.

    Args:
        secret_name: Name of the secret in AWS Secrets Manager

    Returns:
        Parsed JSON data as a dictionary
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
                if not isinstance(parsed_data, dict):
                    raise ValueError("Secret JSON is not a dictionary")
                return parsed_data
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON in secret {secret_name}: {e}") from e
        else:
            raise ValueError("Secret is not in string format")
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            raise ValueError(f"Secret {secret_name} not found") from e
        elif e.response["Error"]["Code"] == "InvalidRequestException":
            raise ValueError(f"Invalid request for secret {secret_name}") from e
        elif e.response["Error"]["Code"] == "InvalidParameterException":
            raise ValueError(f"Invalid parameter for secret {secret_name}") from e
        else:
            raise RuntimeError(f"Error retrieving secret {secret_name}: {e}") from e
