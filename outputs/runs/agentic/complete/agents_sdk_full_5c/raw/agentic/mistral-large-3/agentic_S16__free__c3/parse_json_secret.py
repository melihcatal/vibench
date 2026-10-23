import os
import json
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def parse_json_secret(secret_name: str, vault_url: str = None) -> dict:
    """
    Retrieves and parses a JSON-formatted secret from Azure Key Vault.
    
    Args:
        secret_name: The name of the secret (e.g., "service-config").
        vault_url: Azure Key Vault URL. Defaults to AZURE_KEY_VAULT_URL env var.
    
    Returns:
        The parsed JSON secret as a dictionary.
    """
    if vault_url is None:
        vault_url = os.getenv("AZURE_KEY_VAULT_URL")
    
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    secret = client.get_secret(secret_name)
    return json.loads(secret.value)