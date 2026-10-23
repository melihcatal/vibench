import json
import os
from typing import Dict, Any
from security_client import get_secrets_manager_client


def get_json_secret(secret_name: str) -> Dict[str, Any]:
    """
    Retrieves a secret from AWS Secrets Manager and parses it as JSON.
    """
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    secrets_manager_client = get_secrets_manager_client(region_name=aws_region)

    try:
        get_secret_value_response = secrets_manager_client.get_secret_value(
            SecretId=secret_name
        )
    except Exception as e:
        raise e

    if "SecretString" not in get_secret_value_response:
        raise ValueError("Secret does not contain a string value.")

    secret_string = get_secret_value_response["SecretString"]

    try:
        return json.loads(secret_string)
    except json.JSONDecodeError:
        raise ValueError("Failed to parse secret string as JSON.")


if __name__ == "__main__":
    json_secret_name = "my-app/json-config"
    try:
        parsed_secret = get_json_secret(json_secret_name)
        print(f"Successfully fetched and parsed secret: {json_secret_name}")
        # print(f"Secret content: {parsed_secret}")
    except Exception as e:
        print(f"Error getting JSON secret: {e}")
