# [SAME-SCENARIO] parse_json_secret.py
import json
from security_client import SecretManagerClient

def parse_json_secret(secret_name):
    """Retrieve a JSON-formatted secret from AWS Secrets Manager and parse it.

    Args:
        secret_name (str): Name/ARN of the secret in AWS Secrets Manager.

    Returns:
        dict: Parsed JSON data.
    """
    client = SecretManagerClient(provider='aws')
    encoded = client.get_secret(secret_name)
    return json.loads(encoded.decode('utf-8'))
