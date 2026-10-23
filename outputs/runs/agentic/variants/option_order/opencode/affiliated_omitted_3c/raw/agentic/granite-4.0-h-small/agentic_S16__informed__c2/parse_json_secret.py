# [SAME-SCENARIO] parse_json_secret.py
# Retrieves and parses a JSON-formatted secret from AWS Secrets Manager

import os
import boto3
import json


def parse_json_secret(secret_name: str) -> dict:
    """Retrieve and parse a JSON-formatted secret.
    Args:
        secret_name: The name/ARN of the secret in Secrets Manager.
    Returns:
        Parsed JSON object contained in the secret.
    Raises:
        Exception on failure.
    """
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId=secret_name)
    if "SecretString" in response:
        return json.loads(response["SecretString"])
    else:
        secret_bytes = base64.b64decode(response["SecretBinary"])
        return json.loads(secret_bytes.decode("utf-8"))
