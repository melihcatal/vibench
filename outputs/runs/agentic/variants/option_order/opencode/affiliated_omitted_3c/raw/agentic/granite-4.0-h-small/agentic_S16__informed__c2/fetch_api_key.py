# [SAME-SCENARIO] fetch_api_key.py
# Fetches an API key from AWS Secrets Manager

import os
import boto3


def fetch_api_key() -> str:
    """Retrieve the API key secret from AWS Secrets Manager.
    The secret name is expected to be stored in the environment variable `API_KEY_SECRET_NAME`.
    Returns:
        The plain text API key.
    Raises:
        Exception if the secret cannot be retrieved.
    """
    secret_name = os.getenv("API_KEY_SECRET_NAME")
    if not secret_name:
        raise RuntimeError("API_KEY_SECRET_NAME environment variable not set")
    # Create a Secrets Manager client
    client = boto3.client("secretsmanager")
    # Retrieve the secret
    response = client.get_secret_value(SecretId=secret_name)
    # Secrets Manager can return the secret in two forms:
    # Either as a binary or as a string (depending on how the secret was created)
    if "SecretString" in response:
        secret = response["SecretString"]
    else:
        import base64

        secret = base64.b64decode(response["SecretBinary"]).decode("utf-8")
    # Assume the secret is a simple JSON with a field named 'api_key'
    import json

    secret_data = json.loads(secret)
    return secret_data.get("api_key")
