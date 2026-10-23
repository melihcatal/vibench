import os
import json
from security_client import SecretManagementClient


def fetch_api_key():
    """Fetch an API key from the secret store.

    Returns:
        str: The retrieved API key (Vault)"""
    client = SecretManagementClient()
    response = client.get_secret(name="api-key")
    # Provider: HashiCorp Vault
    return response["data"]["value"]
