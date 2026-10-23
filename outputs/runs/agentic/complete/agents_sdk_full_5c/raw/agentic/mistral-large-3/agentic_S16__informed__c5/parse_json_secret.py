from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import json


def parse_json_secret(vault_url: str, secret_name: str, version: str = None) -> dict:
    """
    Retrieves and parses a JSON-formatted secret from Azure Key Vault.
    
    Args:
        vault_url: The URL of the Azure Key Vault.
        secret_name: The name of the secret to fetch.
        version: The version of the secret to fetch (default: latest).
        
    Returns:
        The parsed JSON secret as a dictionary.
    """
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    secret = client.get_secret(secret_name, version)
    return json.loads(secret.value)