import os
import json
from typing import Dict, Any
from security_client import get_aws_secrets_manager_client


def parse_json_secret(secret_name: str) -> Dict[str, Any]:
    client = get_aws_secrets_manager_client()
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        if "SecretString" in get_secret_value_response:
            secret_string = get_secret_value_response["SecretString"]
            return json.loads(secret_string)
        else:
            raise ValueError("SecretString not found in the response.")
    except Exception as e:
        raise RuntimeError(
            f"Could not retrieve and parse JSON secret from AWS Secrets Manager: {e}"
        )
