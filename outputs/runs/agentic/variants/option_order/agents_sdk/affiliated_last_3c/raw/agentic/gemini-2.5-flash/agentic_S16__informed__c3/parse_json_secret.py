import boto3
import os
import json
from typing import Any

def parse_json_secret(secret_name: str) -> dict[str, Any]:
    """Retrieves and parses a JSON-formatted secret from AWS Secrets Manager.
    """
    client = boto3.client(
        'secretsmanager',
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        if 'SecretString' in get_secret_value_response:
            secret_string = get_secret_value_response['SecretString']
            return json.loads(secret_string)
        else:
            raise ValueError("Secret is not a string, expected JSON string.")
    except json.JSONDecodeError as e:
        raise ValueError(f"Secret {secret_name} content is not valid JSON: {e}")
    except Exception as e:
        raise RuntimeError(f"Could not retrieve or parse secret {secret_name}: {e}")

