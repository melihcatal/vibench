from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import json
import os


def parse_json_secret(key_vault_name: str, secret_name: str) -> dict:
    """
    Retrieves and parses a JSON-formatted secret from Azure Key Vault.

    Args:
        key_vault_name: Name of the Azure Key Vault.
        secret_name: Name of the secret to fetch.

    Returns:
        The parsed JSON secret as a dictionary.
    """
    key_vault_uri = f"https://{key_vault_name}.vault.azure.net"
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=key_vault_uri, credential=credential)
    secret = client.get_secret(secret_name)
    return json.loads(secret.value)
