import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def parse_json_secret(vault_url: str, secret_name: str) -> dict:
    """Retrieve and parse a JSON-formatted secret from Azure Key Vault.
    Args:
        vault_url: The Key Vault URL (e.g., https://myvault.vault.azure.net/).
        secret_name: Name of the secret containing JSON data.
    Returns:
        Parsed JSON as a Python dict.
    """
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    received = client.get_secret(secret_name)
    secret_value = received.value
    import json

    return json.loads(secret_value)
