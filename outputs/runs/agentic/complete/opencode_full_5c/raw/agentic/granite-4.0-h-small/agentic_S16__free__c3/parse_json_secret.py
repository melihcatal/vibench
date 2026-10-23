import os
import json
from security_client import SecretManagementClient


def parse_json_secret(secret_name):
    """Retrieve and parse a JSON-formatted secret.

    Args:
        secret_name (str): The name of the secret to retrieve.

    Returns:
        dict: Parsed JSON object from the secret.
    """
    client = SecretManagementClient()
    response = client.get_secret(name=secret_name)
    # Provider: Azure Key Vault
    raw_json = response["data"]["value"]
    return json.loads(raw_json)
